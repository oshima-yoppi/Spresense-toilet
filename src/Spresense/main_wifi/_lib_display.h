#ifdef _lib_display_h
#define _lib_display_h
void setup_display();
void disp_image(uint16_t *buf, int offset_x, int offset_y, int target_w, int target_h, bool result);
void disp_image_result(uint16_t *buf, int offset_x, int offset_y, int target_w, int target_h, bool *result_mask);
#endif