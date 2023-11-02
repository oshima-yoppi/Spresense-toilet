#ifdef _lib_detection_h
#define _lib_detection_h
void print(String str);
uint16_t *convert_img(CamImage img);
CamImage convert2Tfinput(CamImage img);
bool *detect_people(uint16_t *buf, float th_detect);
bool *detect_people_(CamImage img, float th_detect);
bool *detection_and(bool *result_mask1, bool *result_mask2);
bool isValid(int x, int y);
void countIslands(int idx, bool *map, bool *visited);
int countDFS(bool *map);
#endif
