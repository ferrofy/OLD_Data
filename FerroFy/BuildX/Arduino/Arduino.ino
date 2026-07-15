#include <DHT.h>

#define DHT_PIN 8
#define DHT_TYPE DHT11
#define MQ2_PIN A0
#define RAIN_PIN A1

const unsigned long READ_INTERVAL_MS = 5000;

DHT dht(DHT_PIN, DHT_TYPE);
unsigned long lastReadAt = 0;

long toCenti(float value)
{
    if (value >= 0)
    {
        return (long)(value * 100.0 + 0.5);
    }

    return (long)(value * 100.0 - 0.5);
}

void setup()
{
    Serial.begin(9600);

    pinMode(MQ2_PIN, INPUT);
    pinMode(RAIN_PIN, INPUT);

    dht.begin();

    Serial.println("FerroFy Sensor Node Started");
}

void loop()
{
    unsigned long now = millis();

    if (lastReadAt == 0 || now - lastReadAt >= READ_INTERVAL_MS)
    {
        lastReadAt = now;
        publishSensorReading();
    }
}

void publishSensorReading()
{
    float temperatureC = dht.readTemperature();
    float humidity = dht.readHumidity();
    int mq2Raw = analogRead(MQ2_PIN);
    int rainRaw = analogRead(RAIN_PIN);

    if (isnan(temperatureC) || isnan(humidity))
    {
        Serial.println("{\"error\":\"DHT_READ_FAILED\"}");
        return;
    }

    long temperatureCenti = toCenti(temperatureC);
    long humidityCenti = (long)toCenti(humidity);
    long mq2Centi = (long)mq2Raw * 100L;
    long rainCenti = (long)rainRaw * 100L;

    Serial.print("{\"temperatureCenti\":");
    Serial.print(temperatureCenti);
    Serial.print(",\"humidityCenti\":");
    Serial.print(humidityCenti);
    Serial.print(",\"mq2Centi\":");
    Serial.print(mq2Centi);
    Serial.print(",\"rainCenti\":");
    Serial.print(rainCenti);
    Serial.println("}");
}