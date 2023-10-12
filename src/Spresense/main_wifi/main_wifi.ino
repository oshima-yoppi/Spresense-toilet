#include <Camera.h>
// c:\Users\oosim\Documents\Arduino
#include "tensorflow/lite/micro/all_ops_resolver.h"
#include "tensorflow/lite/micro/micro_error_reporter.h"
#include "tensorflow/lite/micro/micro_interpreter.h"
#include "tensorflow/lite/micro/system_setup.h"
#include "tensorflow/lite/schema/schema_generated.h"
#include "impulse.h"
#include <HttpGs2200.h>
#include <TelitWiFi.h>
#include "config.h"
// tuusin

#define CONSOLE_BAUDRATE 115200
#define SPRESENSE_ID 1
typedef enum
{
    POST = 0,
    GET
} DEMO_STATUS_E;

DEMO_STATUS_E httpStat;
char sendData[100];

int id = 2;
int num = 10;

const uint16_t RECEIVE_PACKET_SIZE = 1500;
uint8_t Receive_Data[RECEIVE_PACKET_SIZE] = {0};

TelitWiFi gs2200;
TWIFI_Params gsparams;
HttpGs2200 theHttpGs2200(&gs2200);
HTTPGS2200_HostParams hostParams;

void parse_httpresponse(char *message)
{
    char *p;

    if ((p = strstr(message, "200 OK\r\n")) != NULL)
    {
        ConsolePrintf("Response : %s\r\n", p + 8);
    }
}

void setup_wifi()
{

    /* initialize digital pin LED_BUILTIN as an output. */
    pinMode(LED0, OUTPUT);
    digitalWrite(LED0, LOW);        // turn the LED off (LOW is the voltage level)
    Serial.begin(CONSOLE_BAUDRATE); // talk to PC

    /* Initialize SPI access of GS2200 */
    Init_GS2200_SPI_type(iS110B_TypeC);

    /* Initialize AT Command Library Buffer */
    gsparams.mode = ATCMD_MODE_STATION;
    gsparams.psave = ATCMD_PSAVE_DEFAULT;
    if (gs2200.begin(gsparams))
    {
        ConsoleLog("GS2200 Initilization Fails");
        while (1)
            ;
    }

    /* GS2200 Association to AP */
    if (gs2200.activate_station(AP_SSID, PASSPHRASE))
    {
        ConsoleLog("Association Fails");
        while (1)
            ;
    }

    hostParams.host = (char *)HTTP_SRVR_IP;
    hostParams.port = (char *)HTTP_PORT;
    theHttpGs2200.begin(&hostParams);

    ConsoleLog("Start HTTP Client");

    /* Set HTTP Headers */
    theHttpGs2200.config(HTTP_HEADER_AUTHORIZATION, "Basic dGVzdDp0ZXN0MTIz");
    theHttpGs2200.config(HTTP_HEADER_TRANSFER_ENCODING, "chunked");
    theHttpGs2200.config(HTTP_HEADER_CONTENT_TYPE, "application/x-www-form-urlencoded");
    theHttpGs2200.config(HTTP_HEADER_HOST, HTTP_SRVR_IP);

    digitalWrite(LED0, HIGH); // turn on LED
}

bool send_data_wifi(int count)
{
    httpStat = POST;
    bool result_wifi = false;
    // static int count = 0;
    int send_data = 100 * SPRESENSE_ID + count;
    switch (httpStat)
    {
    case POST:
        theHttpGs2200.config(HTTP_HEADER_TRANSFER_ENCODING, "chunked");
        // create post data.
        snprintf(sendData, sizeof(sendData), "data=%d", send_data);
        result_wifi = theHttpGs2200.post(HTTP_POST_PATH, sendData);
        if (false == result_wifi)
        {
            break;
        }

        do
        {
            result_wifi = theHttpGs2200.receive(5000);
            if (result_wifi)
            {
                theHttpGs2200.read_data(Receive_Data, RECEIVE_PACKET_SIZE);
                ConsolePrintf("%s", (char *)(Receive_Data));
            }
            else
            {
                // AT+HTTPSEND command is done
                ConsolePrintf("\r\n");
            }
        } while (result_wifi);

        result_wifi = theHttpGs2200.end();

        return true;
    default:
        return false;
    }
}
//
tflite::ErrorReporter *error_reporter = nullptr;
const tflite::Model *model = nullptr;
tflite::MicroInterpreter *interpreter = nullptr;
TfLiteTensor *input = nullptr;
TfLiteTensor *output = nullptr;
int inference_count = 0;

constexpr int kTensorArenaSize = (300) * 1024; // 250
uint8_t tensor_arena[kTensorArenaSize];

/* cropping and scaling parameters */
const int offset_x = 32;
const int offset_y = 12;
const int width = 160;
const int height = 120;
const int target_w = 96;
const int target_h = 96;
const int pixfmt = CAM_IMAGE_PIX_FMT_YUV422;
// const int pixfmt = CAM_IMAGE_PIX_FMT_RGB565;
#define OUTPUT_WIDTH 12
#define OUTPUT_HEIGHT 12
// const int OUTPUT_HEIGHT = 12;
bool result_wifi = false;
int output_width, output_height; // 出力されるセグメンテーションサイズ

void setup()
{
    Serial.begin(115200);
    setup_display();
    CamErr err;

    tflite::InitializeTarget();
    memset(tensor_arena, 0, kTensorArenaSize * sizeof(uint8_t));

    // Set up logging.
    static tflite::MicroErrorReporter micro_error_reporter;
    error_reporter = &micro_error_reporter;

    // Map the model into a usable data structure..
    model = tflite::GetModel(model_tflite);
    if (model->version() != TFLITE_SCHEMA_VERSION)
    {
        Serial.println("Model provided is schema version " + String(model->version()) + " not equal " + "to supported version " + String(TFLITE_SCHEMA_VERSION));
        return;
    }
    else
    {
        Serial.println("Model version: " + String(model->version()));
    }
    // This pulls in all the operation implementations we need.
    static tflite::AllOpsResolver resolver;

    // Build an interpreter to run the model with.
    static tflite::MicroInterpreter static_interpreter(
        model, resolver, tensor_arena, kTensorArenaSize, error_reporter);
    interpreter = &static_interpreter;

    // Allocate memory from the tensor_arena for the model's tensors.
    TfLiteStatus allocate_status = interpreter->AllocateTensors();
    if (allocate_status != kTfLiteOk)
    {
        Serial.println("AllocateTensors() failed");
        return;
    }
    else
    {
        Serial.println("AllocateTensor() Success");
    }

    size_t used_size = interpreter->arena_used_bytes();
    Serial.println("Area used bytes: " + String(used_size));
    input = interpreter->input(0);
    output = interpreter->output(0);

    Serial.println("Model input:");
    Serial.println("dims->size: " + String(input->dims->size));
    for (int n = 0; n < input->dims->size; ++n)
    {
        Serial.println("dims->data[" + String(n) + "]: " + String(input->dims->data[n]));
    }

    Serial.println("Model output:");
    Serial.println("dims->size: " + String(output->dims->size));
    for (int n = 0; n < output->dims->size; ++n)

    {
        Serial.println("dims->data[" + String(n) + "]: " + String(output->dims->data[n]));
    }
    output_width = output->dims->data[2];
    output_height = output->dims->data[1];

    Serial.println("Completed tensorflow setup");
    digitalWrite(LED0, HIGH);

    setup_camera();
    // setup_eltres();
    setup_wifi();
}

void loop()
{
    print("call takePicture");
    CamImage img = take_picture();

    uint16_t *sbuf = convert_img(img);
    // CamImage tf_input = convert2Tfinput(img);
    // bool *result_mask = detect_people_(tf_input, 0.7);
    bool *result_mask = detect_people(sbuf, 0.7);
    disp_image_result(sbuf, 0, 0, target_w, target_h, result_mask);
    int num_people = count_people(result_mask);
    free(result_mask);

    /////通信開始！！！！！
    send_data_wifi(num_people);
    delay(0);
}
