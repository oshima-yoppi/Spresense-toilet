int read_spresense_id(const char *path)
{
    SDClass SD;
    File file;
    Serial.print("Insert SD card.");
    while (!SD.begin())
    {
        ; /* wait until SD card is mounted. */
    }
    Serial.print("SD card is mounted.");
    file = SD.open(path);
    if (!file)
    {
        Serial.println("file open error");
        return -1;
    }
    String str = file.readStringUntil('\n');
    file.close();
    return str.toInt();
}