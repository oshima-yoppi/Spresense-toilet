#ifdef detection_h
#define detection_h

#include <Camera.h>
void print(String str);

int16_t *convert_img(CamImage img);
int detect_people(int16_t *sbuf, float th_detect = 0.5);

#endif