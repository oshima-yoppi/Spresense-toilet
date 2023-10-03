
void setup()
{
  Serial.begin(115200);
}
void loop()
{
    int count = 0;
    for (int i = 0; i < 100; i++)
    {
        count++;
        Serial.println(String(count));
        count = add(count);
        Serial.println(String(count) + " is added");
    }
}