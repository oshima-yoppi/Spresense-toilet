#ifdef _lib_wifi_h
#else
void parse_httpresponse(char *message);
void setup_wifi();
bool send_data_wifi(int count, int spresense_id);
#endif