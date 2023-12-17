// #include <Camera.h>
// #include "_lib_detection.h"

#define OUTPUT_WIDTH 12
#define OUTPUT_HEIGHT 12
void print(String str)
{
    Serial.println(str);
}

uint16_t *convert_img(CamImage img)
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
    uint16_t *sbuf = (uint16_t *)small.getImgBuff();
    return sbuf;
}
CamImage convert2Tfinput(CamImage img)
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
    return small;
}

bool *detect_people(uint16_t *buf, float th_detect)
{
    // int count_people = 0;
    // tfliteに入力するために、データ構造を変換＆正規化スル。
    // カメラから直接得られる画像smallと、tfliteに入力するinputのデータ構造は異なる。(参考書「spresenseで始める～～」p 180参照)
    // input = interpreter->input(0);
    // output = interpreter->output(0);
    int n = 0;
    for (int y = 0; y < target_h; y++)
    {
        for (int x = 0; x < target_w; x++)
        {
            uint16_t value = buf[y * target_w + x];
            float r = (float)((value >> 11) & 0x1F) * 255 / 31;
            float g = (float)((value >> 5) & 0x3F) * 255 / 63;
            float b = (float)((value >> 0) & 0x1F) * 255 / 31;
            // value = (y_h | y_l); /* luminance data */
            float luminance = 0.299 * r + 0.587 * g + 0.114 * b;

            /* set the grayscale data to the input buffer for TensorFlow  */
            luminance -= 128;
            input->data.int8[n++] = (int8_t)luminance;
            // Serial.println(String(input->data.f[n - 1]) + ", ");
        }
        // print("\n改行されたよ");
    }
    // print("-----------");

    bool result = false;
    // disp_image(sbuf, 0, 0, target_w, target_h, result);
    Serial.println("Do inference");
    TfLiteStatus invoke_status = interpreter->Invoke();
    if (invoke_status != kTfLiteOk)
    {
        Serial.println("Invoke failed");
        return;
    }

    std::pair<int, int> directions[4] = {{1, 0}, {0, 1}, {-1, 0}, {0, -1}};
    // UnionFind uf(OUTPUT_WIDTH * OUTPUT_HEIGHT);
    bool *result_mask = new bool[OUTPUT_WIDTH * OUTPUT_HEIGHT];
    int idx = 1;
    for (int y = 0; y < output_height; ++y)
    {
        for (int x = 0; x < output_width; ++x)
        {
            int8_t output_value = output->data.int8[idx];

            float value = output_value + 128;
            value /= 255.0;
            // int value = output->data.f[y * output_width + x];
            // value += 128;
            // value /= 255.0;
            // Serial.print(String(value) + ", ");
            if (value >= th_detect)
            {
                result_mask[y * output_width + x] = true;
            }
            else
            {
                result_mask[y * output_width + x] = false;
            }
            idx += 2;
        }
        Serial.println("\n");
    }
    return result_mask;
}

bool *detect_people_(CamImage tfinput, float th_detect)
{
    // int count_people = 0;
    // tfliteに入力するために、データ構造を変換＆正規化スル。
    // カメラから直接得られる画像smallと、tfliteに入力するinputのデータ構造は異なる。(参考書「spresenseで始める～～」p 180参照)
    uint16_t *buf = (uint16_t *)tfinput.getImgBuff();
    int n = 0;
    for (int y = 0; y < target_h; y++)
    {
        for (int x = 0; x < target_w; x++)
        {
            uint16_t value = buf[y * target_w + x];
            uint16_t y_h = (value & 0xf000) >> 8;
            uint16_t y_l = (value & 0x00f0) >> 4;
            value = (y_h | y_l); /* luminance data */
            /* set the grayscale data to the input buffer for TensorFlow  */
            input->data.f[n++] = (uint8_t)value;
        }
    }
    print("luminance" + String(input->data.f[0]));

    bool result = false;
    // disp_image(sbuf, 0, 0, target_w, target_h, result);
    Serial.println("Do inference");
    TfLiteStatus invoke_status = interpreter->Invoke();
    if (invoke_status != kTfLiteOk)
    {
        Serial.println("Invoke failed");
        return;
    }

    std::pair<int, int> directions[4] = {{1, 0}, {0, 1}, {-1, 0}, {0, -1}};
    // UnionFind uf(OUTPUT_WIDTH * OUTPUT_HEIGHT);
    bool *result_mask = new bool[OUTPUT_WIDTH * OUTPUT_HEIGHT];
    int idx = 1;
    for (int y = 0; y < output_height; ++y)
    {
        for (int x = 0; x < output_width; ++x)
        {
            float value = output->data.uint8[idx];
            // int value = output->data.f[y * output_width + x];
            value /= 255.0;
            Serial.print(String(value) + ", ");
            if (value >= th_detect)
            {
                result_mask[y * output_width + x] = true;
            }
            else
            {
                result_mask[y * output_width + x] = false;
            }
            idx += 2;
        }
        Serial.println("\n");
    }
    return result_mask;
}

bool *detection_and(bool *result1, bool *result2)
{
    bool *result_mask = new bool[OUTPUT_WIDTH * OUTPUT_HEIGHT];
    for (int i = 0; i < OUTPUT_WIDTH * OUTPUT_HEIGHT; i++)
    {
        result_mask[i] = result1[i] && result2[i];
        if (result_mask[i] == true)
        {
            Serial.println("true");
        }
    }
    return result_mask;
}

const int dx[] = {-1, 1, 0, 0};
const int dy[] = {0, 0, -1, 1};
// 与えられた座標が有効かどうかを確認する関数
bool isValid(int x, int y)
{
    return x >= 0 && x < OUTPUT_WIDTH && y >= 0 && y < OUTPUT_HEIGHT;
}
void countIslands(int idx, bool *map, bool *visited)
{
    visited[idx] = true;

    int x = idx % OUTPUT_WIDTH;
    int y = idx / OUTPUT_WIDTH;

    for (int i = 0; i < 4; ++i)
    {
        int newX = x + dx[i];
        int newY = y + dy[i];
        int newIdx = newY * OUTPUT_WIDTH + newX;

        if (isValid(newX, newY) && map[newIdx] && !visited[newIdx])
        {
            countIslands(newIdx, map, visited);
        }
    }
}
// 繋がっているところをdfs使ってカウントする関数
int countDFS(bool *map)
{
    int count = 0;
    bool visited[OUTPUT_WIDTH * OUTPUT_HEIGHT] = {false};
    for (int i = 0; i < OUTPUT_WIDTH * OUTPUT_HEIGHT; ++i)
    {
        if (map[i] && !visited[i])
        {
            countIslands(i, map, visited);
            count++;
        }
    }

    return count;
}