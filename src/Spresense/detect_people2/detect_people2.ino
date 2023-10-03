#include <Camera.h>
// c:\Users\oosim\Documents\Arduino
#include "tensorflow/lite/micro/all_ops_resolver.h"
#include "tensorflow/lite/micro/micro_error_reporter.h"
#include "tensorflow/lite/micro/micro_interpreter.h"
#include "tensorflow/lite/micro/system_setup.h"
#include "tensorflow/lite/schema/schema_generated.h"
#include "src/_lib_camera.h"
#include "_lib_detection.h"
// #include <vector>
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

constexpr int kTensorArenaSize = (500) * 1024; // 250
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

/* callback function of the camera streaming */
/* the inference process is done in this function */
struct UnionFind
{
    int parent[OUTPUT_WIDTH * OUTPUT_HEIGHT] = {};
    int rank[OUTPUT_WIDTH * OUTPUT_HEIGHT] = {};
    UnionFind(int n)
    {
        for (int i = 0; i < n; i++)
        {
            parent[i] = i;
            rank[i] = 0;
        }
    }
    int find(int x)
    {
        if (parent[x] == x)
        {
            return x;
        }
        else
        {
            return parent[x] = find(parent[x]);
        }
    }
    void unite(int x, int y)
    {
        x = find(x);
        y = find(y);
        if (x == y)
        {
            return;
        }
        if (rank[x] < rank[y])
        {
            parent[x] = y;
        }
        else
        {
            parent[y] = x;
            if (rank[x] == rank[y])
            {
                rank[x]++;
            }
        }
    }
    bool same(int x, int y)
    {
        return find(x) == find(y);
    }
    int count()
    {
        int cnt = 0;
        for (int i = 0; i < OUTPUT_WIDTH * OUTPUT_HEIGHT; i++)
        {
            if (parent[i] == i)
            {
                cnt++;
            }
        }
        return cnt;
    }
};
// void print(String str)
// {
//     Serial.println(str);
// }

// void CamCB(CamImage img)
// {
//     static uint32_t last_mills = 0;

//     if (!img.isAvailable())
//     {
//         Serial.println("img is not available");
//         return;
//     }

//     // 画像をクリッピングをしてRGBフォーマットに変換。
//     CamImage small;
//     CamErr err = img.clipAndResizeImageByHW(small,
//                                             offset_x, offset_y,
//                                             offset_x + target_w - 1,
//                                             offset_y + target_h - 1,
//                                             target_w, target_h);

//     small.convertPixFormat(CAM_IMAGE_PIX_FMT_RGB565);

//     int16_t *sbuf = (uint16_t *)small.getImgBuff();
//     if (err != CAM_ERR_SUCCESS)
//     {
//         Serial.println("clipAndResizeImageByHW err: " + String(err));
//         return;
//     }

//     // tfliteに入力するために、データ構造を変換＆正規化スル。
//     // カメラから直接得られる画像smallと、tfliteに入力するinputのデータ構造は異なる。(参考書「spresenseで始める～～」p 180参照)
//     int n = 0;
//     float *fbuf_r = input->data.f + target_h * target_w * 0;
//     float *fbuf_g = input->data.f + target_h * target_w * 1;
//     float *fbuf_b = input->data.f + target_h * target_w * 2;
//     for (int y = 0; y < target_h; y++)
//     {
//         for (int x = 0; x < target_w; x++)
//         {
//             uint16_t value = sbuf[y * target_w + x];
//             float r = (float)((value >> 11) & 0x1F) / 31.0;
//             float g = (float)((value >> 5) & 0x3F) / 63.0;
//             float b = (float)((value >> 0) & 0x1F) / 31.0;
//             fbuf_r[n] = r;
//             fbuf_g[n] = g;
//             fbuf_b[n] = b;
//             n++;
//         }
//     }

//     bool result = false;
//     disp_image(sbuf, 0, 0, target_w, target_h, result);
//     Serial.println("Do inference");
//     TfLiteStatus invoke_status = interpreter->Invoke();
//     if (invoke_status != kTfLiteOk)
//     {
//         Serial.println("Invoke failed");
//         return;
//     }
//     for (int y = 0; y < output_height; ++y)
//     {
//         for (int x = 0; x < output_width; ++x)
//         {
//             // uint8_t value = output->data.uint8[y * output_width + x];
//             float value = output->data.f[y * output_width + x];

//             Serial.print(String(value) + ", ");
//         }
//         Serial.println("\n");
//     }

//     uint32_t current_mills = millis();
//     uint32_t duration = current_mills - last_mills;
//     Serial.println("duration = " + String(duration));
//     last_mills = current_mills;
// }

// int16_t *convert_img(CamImage img)
// {
//     if (!img.isAvailable())
//     {
//         Serial.println("img is not available");
//         return;
//     }

//     // 画像をクリッピングをしてRGBフォーマットに変換。
//     CamImage small;
//     CamErr err = img.clipAndResizeImageByHW(small,
//                                             offset_x, offset_y,
//                                             offset_x + target_w - 1,
//                                             offset_y + target_h - 1,
//                                             target_w, target_h);

//     small.convertPixFormat(CAM_IMAGE_PIX_FMT_RGB565);
//     int16_t *sbuf = (uint16_t *)small.getImgBuff();
//     return sbuf;
// }

// int detect_people(int16_t *sbuf, float th_detect = 0.5)
// {
//     // int count_people = 0;
//     // tfliteに入力するために、データ構造を変換＆正規化スル。
//     // カメラから直接得られる画像smallと、tfliteに入力するinputのデータ構造は異なる。(参考書「spresenseで始める～～」p 180参照)
//     int n = 0;
//     float *fbuf_r = input->data.f + target_h * target_w * 0;
//     float *fbuf_g = input->data.f + target_h * target_w * 1;
//     float *fbuf_b = input->data.f + target_h * target_w * 2;
//     for (int y = 0; y < target_h; y++)
//     {
//         for (int x = 0; x < target_w; x++)
//         {
//             uint16_t value = sbuf[y * target_w + x];
//             float r = (float)((value >> 11) & 0x1F) / 31.0;
//             float g = (float)((value >> 5) & 0x3F) / 63.0;
//             float b = (float)((value >> 0) & 0x1F) / 31.0;
//             fbuf_r[n] = r;
//             fbuf_g[n] = g;
//             fbuf_b[n] = b;
//             n++;
//         }
//     }

//     bool result = false;
//     disp_image(sbuf, 0, 0, target_w, target_h, result);
//     Serial.println("Do inference");
//     TfLiteStatus invoke_status = interpreter->Invoke();
//     if (invoke_status != kTfLiteOk)
//     {
//         Serial.println("Invoke failed");
//         return;
//     }

//     std::pair<int, int> directions[4] = {{1, 0}, {0, 1}, {-1, 0}, {0, -1}};
//     UnionFind uf(OUTPUT_WIDTH * OUTPUT_HEIGHT);

//     for (int y = 0; y < output_height; ++y)
//     {
//         for (int x = 0; x < output_width; ++x)
//         {
//             // uint8_t value = output->data.uint8[y * output_width + x];
//             float value = output->data.f[y * output_width + x];

//             Serial.print(String(value) + ", ");
//             if (value >= th_detect)
//             {
//                 for (auto dir : directions)
//                 {
//                     int nx = x + dir.first;
//                     int ny = y + dir.second;
//                     if (nx < 0 || nx >= output_width || ny < 0 || ny >= output_height)
//                     {
//                         continue;
//                     }
//                     if (output->data.f[ny * output_width + nx] >= th_detect)
//                     {
//                         uf.unite(y * output_width + x, ny * output_width + nx);
//                     }
//                 }
//             }
//         }
//         Serial.println("\n");
//     }
//     int count_people = uf.count();
//     print("!!!!!!!!!!count_people = " + String(count_people));
//     return count_people;
// }

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

    int16_t *sbuf = convert_img(img);
    disp_image(sbuf, 0, 0, target_w, target_h, result);

    int count_people = detect_people_(sbuf, 0.9);
    print("count_people = " + String(count_people));

    // delay(1000);
}
