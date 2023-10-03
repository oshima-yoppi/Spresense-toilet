#include <Camera.h>
#include "_lib_detection.h"
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

int detect_people(int16_t *sbuf, float th_detect = 0.5)
{
    // int count_people = 0;
    // tfliteに入力するために、データ構造を変換＆正規化スル。
    // カメラから直接得られる画像smallと、tfliteに入力するinputのデータ構造は異なる。(参考書「spresenseで始める～～」p 180参照)
    int n = 0;
    float *fbuf_r = input->data.f + target_h * target_w * 0;
    float *fbuf_g = input->data.f + target_h * target_w * 1;
    float *fbuf_b = input->data.f + target_h * target_w * 2;
    for (int y = 0; y < target_h; y++)
    {
        for (int x = 0; x < target_w; x++)
        {
            uint16_t value = sbuf[y * target_w + x];
            float r = (float)((value >> 11) & 0x1F) / 31.0;
            float g = (float)((value >> 5) & 0x3F) / 63.0;
            float b = (float)((value >> 0) & 0x1F) / 31.0;
            fbuf_r[n] = r;
            fbuf_g[n] = g;
            fbuf_b[n] = b;
            n++;
        }
    }

    bool result = false;
    disp_image(sbuf, 0, 0, target_w, target_h, result);
    Serial.println("Do inference");
    TfLiteStatus invoke_status = interpreter->Invoke();
    if (invoke_status != kTfLiteOk)
    {
        Serial.println("Invoke failed");
        return;
    }

    std::pair<int, int> directions[4] = {{1, 0}, {0, 1}, {-1, 0}, {0, -1}};
    UnionFind uf(OUTPUT_WIDTH * OUTPUT_HEIGHT);

    for (int y = 0; y < output_height; ++y)
    {
        for (int x = 0; x < output_width; ++x)
        {
            // uint8_t value = output->data.uint8[y * output_width + x];
            float value = output->data.f[y * output_width + x];

            Serial.print(String(value) + ", ");
            if (value >= th_detect)
            {
                for (auto dir : directions)
                {
                    int nx = x + dir.first;
                    int ny = y + dir.second;
                    if (nx < 0 || nx >= output_width || ny < 0 || ny >= output_height)
                    {
                        continue;
                    }
                    if (output->data.f[ny * output_width + nx] >= th_detect)
                    {
                        uf.unite(y * output_width + x, ny * output_width + nx);
                    }
                }
            }
        }
        Serial.println("\n");
    }
    int count_people = uf.count();
    print("!!!!!!!!!!count_people = " + String(count_people));
    return count_people;
}
