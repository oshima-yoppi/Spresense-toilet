#include <Camera.h>
#include "_lib_camera.h"
void setup_camera()
{
    CamErr err;
    Serial.println("Prepare camera");
    err = theCamera.begin();
    if (err != CAM_ERR_SUCCESS)
    {
        Serial.println("begin err: " + String(err));
    }
    err = theCamera.setAutoWhiteBalanceMode(CAM_WHITE_BALANCE_DAYLIGHT);
    if (err != CAM_ERR_SUCCESS)
    {
        Serial.println("setAutoWhiteBalanceMode err: " + String(err));
    }
    err = theCamera.setStillPictureImageFormat(
        width, height, pixfmt);
    if (err != CAM_ERR_SUCCESS)
    {
        Serial.println("setStillPictureImageFormat err: " + String(err));
        return;
    }
    Serial.println("finish camera setup!!");
}
CamImage take_picture()
{
    CamImage img = theCamera.takePicture();
    if (!img.isAvailable())
    {
        print("img is not available");
    }
    return img;
}
