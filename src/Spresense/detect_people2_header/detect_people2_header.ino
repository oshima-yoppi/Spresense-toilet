#include <Camera.h>
// c:\Users\oosim\Documents\Arduino
#include "tensorflow/lite/micro/all_ops_resolver.h"
#include "tensorflow/lite/micro/micro_error_reporter.h"
#include "tensorflow/lite/micro/micro_interpreter.h"
#include "tensorflow/lite/micro/system_setup.h"
#include "tensorflow/lite/schema/schema_generated.h"
// include "Adafruit_Thermal.h"
#include "Adafruit_GFX.h"
#include "Adafruit_ILI9341.h"
// uint32_t color_codes[] = {ILI9341_ORANGE};
// #include "spresense_model_quant.h"
#include "_lib_display.h"
#include "_lib_camera.h"
#include "_lib_detection.h"
#include "impulse.h"
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
bool result = false;
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
    free(result_mask);
    // free(sbuf);

    delay(0);
}
