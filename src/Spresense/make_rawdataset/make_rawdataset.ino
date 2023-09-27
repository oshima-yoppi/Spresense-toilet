#include <Camera.h>

// #include "tensorflow/lite/micro/all_ops_resolver.h"
// #include "tensorflow/lite/micro/micro_error_reporter.h"
// #include "tensorflow/lite/micro/micro_interpreter.h"
// #include "tensorflow/lite/micro/system_setup.h"
// #include "tensorflow/lite/schema/schema_generated.h"
#include <stdio.h>
#include <SDHCI.h>

SDClass theSD;

int inference_count = 0;

/* cropping and scaling parameters */
const int offset_x = 32;
const int offset_y = 12;
const int width = 160;
const int height = 120;
const int target_w = 96;
const int target_h = 96;
const int yuv_pixfmt = CAM_IMAGE_PIX_FMT_YUV422;
const int jpg_pixfmt = CAM_IMAGE_PIX_FMT_JPG;
const int rgb_pixfmt = CAM_IMAGE_PIX_FMT_RGB565;
const int OUTPUT_WIDTH = 12;
const int OUTPUT_HEIGHT = 12;
bool result = false;
int cam_count = 0;
int output_width, output_height; // 出力されるセグメンテーションサイズ

/* callback function of the camera streaming */
/* the inference process is done in this function */
void print(String str)
{
    Serial.println(str);
}

int16_t *convert_img(CamImage img)
{
    if (!img.isAvailable())
    {
        Serial.println("img is not available");
        return;
    }

    // 画像をクリッピングをしてRGBフォーマットに変換。
    CamImage small;
    CamErr err = img.clipAndResizeImageByHW(small,
                                            offset_x, offset_y,
                                            offset_x + target_w - 1,
                                            offset_y + target_h - 1,
                                            target_w, target_h);

    small.convertPixFormat(CAM_IMAGE_PIX_FMT_RGB565);
    int16_t *sbuf = (uint16_t *)small.getImgBuff();
    return sbuf;
}
CamImage resize_and_crop_img(CamImage img)
{
    if (!img.isAvailable())
    {
        Serial.println("img is not available");
        return;
    }

    // 画像をクリッピングをしてRGBフォーマットに変換。
    CamImage small;
    CamErr err = img.clipAndResizeImageByHW(small,
                                            offset_x, offset_y,
                                            offset_x + target_w - 1,
                                            offset_y + target_h - 1,
                                            target_w, target_h);
    if (err != CAM_ERR_SUCCESS)
    {
        Serial.println("clipAndResizeImageByHW err: " + String(err));
        return;
    }

    return small;
}

void setup()
{
    Serial.begin(115200);
    setup_display();
    CamErr err;

    digitalWrite(LED0, HIGH);
    setup_camera();
    while (!theSD.begin())
    {
    }
}
void loop()
{

    print("call takePicture");
    CamImage img = take_picture();
    CamImage small_img = resize_and_crop_img(img);

    if (small_img.isAvailable())
    {
        print("call disp_image");
        char filename[16] = {0};
        sprintf(filename, "PICT%03d.JPG", cam_count);
        int16_t *sbuf = convert_img(img);
        if (theSD.exists(filename))
        {
            theSD.remove(filename);
        }

        disp_image(sbuf, 0, 0, target_w, target_h, result);
        small_img.convertPixFormat(CAM_IMAGE_PIX_FMT_JPG);
        File myFile = theSD.open(filename, FILE_WRITE);
        myFile.write(small_img.getImgBuff(), small_img.getImgSize());
        myFile.close();
        ++cam_count;
    }
}