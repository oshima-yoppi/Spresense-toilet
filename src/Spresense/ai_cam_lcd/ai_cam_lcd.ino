#include <Camera.h>

#include "tensorflow/lite/micro/all_ops_resolver.h"
#include "tensorflow/lite/micro/micro_error_reporter.h"
#include "tensorflow/lite/micro/micro_interpreter.h"
#include "tensorflow/lite/micro/system_setup.h"
#include "tensorflow/lite/schema/schema_generated.h"
// #include <spreseense_inferencing.h>
// #include "Dental_Model_Classifier_inferencing.h"

// #include "spresense_model_gomi.h"
#include "spresense_model_quant.h"
// #include "person_detect_model.h"
tflite::ErrorReporter *error_reporter = nullptr;
const tflite::Model *model = nullptr;
tflite::MicroInterpreter *interpreter = nullptr;
TfLiteTensor *input = nullptr;
TfLiteTensor *output = nullptr;
int inference_count = 0;

constexpr int kTensorArenaSize = (600) * 1024; // 250
uint8_t tensor_arena[kTensorArenaSize];

/* cropping and scaling parameters */
const int offset_x = 32;
const int offset_y = 12;
const int width = 160;
const int height = 120;
const int target_w = 96;
const int target_h = 96;
const int pixfmt = CAM_IMAGE_PIX_FMT_YUV422;
const int OUTPUT_WIDTH = 4;
const int OUTPUT_HEIGHT = 4;

int output_width, output_height; // 出力されるセグメンテーションサイズ

/* callback function of the camera streaming */
/* the inference process is done in this function */
void CamCB(CamImage img)
{
    static uint32_t last_mills = 0;

    if (!img.isAvailable())
    {
        Serial.println("img is not available");
        return;
    }

    uint16_t *sbuf = (uint16_t *)img.getImgBuff();
    int n = 0;
    for (int y = offset_y; y < offset_y + target_h; ++y)
    {
        for (int x = offset_x; x < offset_x + target_w; ++x)
        {
            /* extracting luminance data from YUV422 data */
            uint16_t value = sbuf[y * width + x];
            float r = (float)((value >> 11) & 0x1F) / 31.0;
            float g = (float)((value >> 5) & 0x3F) / 63.0;
            float b = (float)((value >> 0) & 0x1F) / 31.0;

            input->data.f[n + target_h * target_w * 0] = r;
            input->data.f[n + target_h * target_w * 1] = g;
            input->data.f[n + target_h * target_w * 2] = b;
            n++;
        }
    }

    Serial.println("Do inference");
    TfLiteStatus invoke_status = interpreter->Invoke();
    if (invoke_status != kTfLiteOk)
    {
        Serial.println("Invoke failed");
        return;
    }
    for (int y = 0; y < output_height; ++y)
    {
        for (int x = 0; x < output_width; ++x)
        {
            uint8_t value = output->data.uint8[y * output_width + x];

            Serial.print(String(value) + ", ");
        }
        Serial.println("\n");
    }

    /* get the result */
    bool result = false;
    int8_t person_score = output->data.uint8[1];
    int8_t no_person_score = output->data.uint8[0];
    Serial.print("Person = " + String(person_score) + ", ");
    Serial.println("No_person = " + String(no_person_score));
    if ((person_score > no_person_score) && (person_score > 60))
    {
        digitalWrite(LED3, HIGH);
        result = true;
    }
    else
    {
        digitalWrite(LED3, LOW);
    }

    /* display the captured data */
    disp_image(sbuf, offset_x, offset_y, target_w, target_h, result);

    uint32_t current_mills = millis();
    uint32_t duration = current_mills - last_mills;
    Serial.println("duration = " + String(duration));
    last_mills = current_mills;
}

void setup()
{
    Serial.begin(115200);
    setup_display();

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

    CamErr err = theCamera.begin(1, CAM_VIDEO_FPS_15, width, height, pixfmt);
    if (err != CAM_ERR_SUCCESS)
    {
        Serial.println("camera begin err: " + String(err));
        return;
    }
    err = theCamera.startStreaming(true, CamCB); // この関数でずっとカメラの画像を取得し続ける。止めたかったらfalseにする。
    if (err != CAM_ERR_SUCCESS)
    {
        Serial.println("start streaming err: " + String(err));
        return;
    }
}

void loop()
{
}
