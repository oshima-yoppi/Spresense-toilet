#ifdef _lib_eltres_h
#define _lib_eltres_h
void eltres_event_cb(eltres_board_event event);
void gga_event_cb(const eltres_board_gga_info *gga_info);
void setup_eltres();
void send_data(int num_people);
void send_data_eltres(int num_people);
#endif