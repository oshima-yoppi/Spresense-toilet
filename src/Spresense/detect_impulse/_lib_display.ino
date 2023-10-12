// #include "Adafruit_GFX.h"
// #include "Adafruit_ILI9341.h"
// // #include "_lib_display.h"
// #define TFT_RST 8
// #define TFT_DC 9
// #define TFT_CS 10
// Adafruit_ILI9341 display = Adafruit_ILI9341(TFT_CS, TFT_DC, TFT_RST);
// Adafruit_ILI9341 tft = Adafruit_ILI9341(TFT_CS, TFT_DC, TFT_RST);
// // uint16_t disp[target_w * target_h];

// /* indicator box */
// int box_sx = 80;
// int box_ex = 90;
// int box_sy = 5;
// int box_ey = 15;

// void setup_display()
// {
//     // tft.begin();
//     // tft.setRotation(3);
//     display.begin();
//     display.setRotation(3);
// }

// void disp_image(uint16_t *buf, int offset_x, int offset_y, int target_w, int target_h)
// {
//     display.drawRGBBitmap(0, 0, buf, target_w, target_h);
//     return;
// }

// // RGB565カラーフォーマットで色を設定する関数
// void setRGB565Color(uint16_t *buf, int width, int x, int y, uint16_t color)
// {
//     int index = y * width + x;
//     buf[index] = color;
// }
// void disp_image_result(uint16_t *buf, int offset_x, int offset_y, int target_w, int target_h, bool *result_mask)
// {
//     int width_result = OUTPUT_WIDTH;
//     int height_result = OUTPUT_HEIGHT;
//     int width = target_w;
//     int height = target_h;
//     int x_ratio = width / width_result;
//     int y_ratio = height / height_result;

//     uint16_t redColor = 0b11111 << 11;
//     for (int x = 0; x < width_result; x++)
//     {
//         for (int y = 0; y < height_result; y++)
//         {
//             if (result_mask[y * width_result + x])
//             {
//                 int startX = x * x_ratio;
//                 int startY = y * y_ratio;
//                 int endX = startX + x_ratio;
//                 int endY = startY + y_ratio;
//                 for (int i = startX; i < endX; i++)
//                 {
//                     setRGB565Color(buf, width, i, startY, redColor);
//                     setRGB565Color(buf, width, i, endY, redColor);
//                 }
//                 for (int i = startY; i < endY; i++)
//                 {
//                     setRGB565Color(buf, width, startX, i, redColor);
//                     setRGB565Color(buf, width, endX, i, redColor);
//                 }
//             }
//         }
//     }
//     disp_image(buf, offset_x, offset_y, target_w, target_h);
// }