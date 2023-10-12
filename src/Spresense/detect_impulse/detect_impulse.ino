
#include <Camera.h>
#include <Adafruit_GFX.h>
#include <Adafruit_ILI9341.h>
#include "Adafruit_Thermal.h"
#include "data_inferencing.h"

#define EI_CAMERA_RAW_FRAME_BUFFER_COLS 1280
#define EI_CAMERA_RAW_FRAME_BUFFER_ROWS 960
#define CAPTURED_IMAGE_BUFFER_COLS 320
#define CAPTURED_IMAGE_BUFFER_ROWS 320
static uint8_t *ei_camera_capture_out = NULL;

// const int offset_x = 32;
// const int offset_y = 12;
// const int width = 160;
// const int height = 120;
// const int target_w = 96;
// const int target_h = 96;
// const int pixfmt = CAM_IMAGE_PIX_FMT_YUV422;
// // Define the dental model category (class) names and color codes:
const char *classes[] = {"head "};
uint32_t color_codes[] = {ILI9341_GREEN};

// void print(String str)
// {
//     Serial.println(str);
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

// void run_inference_to_make_predictions()
// {
//     // Summarize the Edge Impulse FOMO model inference settings (from model_metadata.h):
//     ei_printf("\nInference settings:\n");
//     ei_printf("\tImage resolution: %dx%d\n", EI_CLASSIFIER_INPUT_WIDTH, EI_CLASSIFIER_INPUT_HEIGHT);
//     ei_printf("\tFrame size: %d\n", EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE);
//     ei_printf("\tNo. of classes: %d\n", sizeof(ei_classifier_inferencing_categories) / sizeof(ei_classifier_inferencing_categories[0]));

//     // Take a picture with the given still picture settings.
//     CamImage img = theCamera.takePicture();

//     if (img.isAvailable())
//     {
//         // Pause video stream and print errors, if any.
//         adjustColor(1, 1, 0);
//         Serial.println("\nPausing streaming...\n");
//         err = theCamera.startStreaming(false, CamCB);
//         if (err != CAM_ERR_SUCCESS)
//             printError(err);

//         // Resize the currently captured image depending on the given FOMO model.
//         CamImage res_img;
//         img.resizeImageByHW(res_img, EI_CLASSIFIER_INPUT_WIDTH, EI_CLASSIFIER_INPUT_HEIGHT);
//         Serial.printf("Captured Image Resolution: %d / %d\nResized Image Resolution: %d / %d", img.getWidth(), img.getHeight(), res_img.getWidth(), res_img.getHeight());

//         // Convert the resized (sample) image data format to GRAYSCALE so as to run inferences with the model.
//         res_img.convertPixFormat(CAM_IMAGE_PIX_FMT_GRAY);
//         Serial.print("\nResized Image Format: ");
//         Serial.println((res_img.getPixFormat() == CAM_IMAGE_PIX_FMT_GRAY) ? "GRAYSCALE" : "ERROR");

//         // Run inference:
//         ei::signal_t signal;
//         ei_camera_capture_out = res_img.getImgBuff();
//         // Create a signal object from the resized and converted sample image.
//         signal.total_length = EI_CLASSIFIER_INPUT_WIDTH * EI_CLASSIFIER_INPUT_HEIGHT;
//         signal.get_data = &ei_camera_cutout_get_data;
//         // Run the classifier:
//         ei_impulse_result_t result = {0};
//         EI_IMPULSE_ERROR _err = run_classifier(&signal, &result, false);
//         if (_err != EI_IMPULSE_OK)
//         {
//             ei_printf("ERR: Failed to run classifier (%d)\n", err);
//             return;
//         }

//         // Print the inference timings on the serial monitor.
//         ei_printf("\nPredictions (DSP: %d ms., Classification: %d ms., Anomaly: %d ms.): \n",
//                   result.timing.dsp, result.timing.classification, result.timing.anomaly);

//         // Obtain the object detection results and bounding boxes for the detected labels (classes).
//         bool bb_found = result.bounding_boxes[0].value > 0;
//         for (size_t ix = 0; ix < EI_CLASSIFIER_OBJECT_DETECTION_COUNT; ix++)
//         {
//             auto bb = result.bounding_boxes[ix];
//             if (bb.value == 0)
//                 continue;
//             // Print the detected bounding box measurements on the serial monitor.
//             ei_printf("    %s (", bb.label);
//             ei_printf_float(bb.value);
//             ei_printf(") [ x: %u, y: %u, width: %u, height: %u ]\n", bb.x, bb.y, bb.width, bb.height);
//             b_b_x = bb.x;
//             b_b_y = bb.y;
//             b_b_w = bb.width;
//             b_b_h = bb.height;
//             // Get the predicted label (class).
//             if (bb.label == "cast")
//                 predicted_class = 0;
//             if (bb.label == "failed")
//                 predicted_class = 1;
//             if (bb.label == "implant")
//                 predicted_class = 2;
//             Serial.print("\nPredicted Class: ");
//             Serial.println(predicted_class);
//         }
//         if (!bb_found)
//             ei_printf("    No objects found!\n");

// // Detect anomalies, if any:
// #if EI_CLASSIFIER_HAS_ANOMALY == 1
//         ei_printf("Anomaly: ");
//         ei_printf_float(result.anomaly);
//         ei_printf("\n");
// #endif

//         // If the Edge Impulse FOMO model predicted a label (class) successfully:
//         if (predicted_class != -1)
//         {
//             // Scale the detected bounding box.
//             int box_scale_x = tft.width() / EI_CLASSIFIER_INPUT_WIDTH;
//             b_b_x = b_b_x * box_scale_x;
//             b_b_w = b_b_w * box_scale_x * 16;
//             if ((b_b_w + b_b_x) > (tft.width() - 10))
//                 b_b_w = tft.width() - b_b_x - 10;
//             int box_scale_y = tft.height() / EI_CLASSIFIER_INPUT_HEIGHT;
//             b_b_y = b_b_y * box_scale_y;
//             b_b_h = b_b_h * box_scale_y * 16;
//             if ((b_b_h + b_b_y) > (tft.height() - 10))
//                 b_b_h = tft.height() - b_b_y - 10;

//             // Display the predicted label (class) and the detected bounding box on the ILI9341 TFT screen.
//             for (int i = 0; i < 5; i++)
//             {
//                 tft.drawRect(b_b_x + i, b_b_y + i, b_b_w - (2 * i), b_b_h - (2 * i), color_codes[predicted_class]);
//             }
//             int c_x = 10, c_y = 10, r_x = 120, r_y = 40, r = 3, offset = 6;
//             tft.drawRGBBitmap(10, c_y + r_y + 10, (uint16_t *)(dental.pixel_data), (int16_t)dental.width, (int16_t)dental.height);
//             tft.fillRoundRect(c_x, c_y, r_x, r_y, r, ILI9341_WHITE);
//             tft.fillRoundRect(c_x + offset, c_y + offset, r_x - (2 * offset), r_y - (2 * offset), r, color_codes[predicted_class]);
//             tft.setTextColor(ILI9341_WHITE);
//             tft.setTextSize(2);
//             tft.setCursor(c_x + (2 * offset), c_y + (2 * offset));
//             tft.printf(classes[predicted_class]);

//             // Print the predicted label (class) information via the thermal printer.
//             print_thermal(predicted_class);

//             // Clear the predicted class (label).
//             predicted_class = -1;
//         }

//         sleep(10);

//         // Resume video stream and print errors, if any.
//         adjustColor(0, 1, 0);
//         sleep(2);
//         Serial.println("\nResuming streaming...\n");
//         err = theCamera.startStreaming(true, CamCB);
//         if (err != CAM_ERR_SUCCESS)
//             printError(err);
//     }
//     else
//     {
//         Serial.println("Failed to take a picture!");
//         adjustColor(1, 0, 0);
//         sleep(2);
//     }
// }

void setup()
{
}
void loop()
{
    run_inference_to_make_predictions();
}