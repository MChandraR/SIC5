#include <ArduinoJson.h>
#include <HTTPClient.h>
#include "WiFi.h"
#include "DHT.h"

const int DHT_PIN = 15;
#define WIFI_SSID "Mcr.net" 
#define WIFI_PASSWORD "nggapakepw" 
#define SERVER_ADDRESS "http://192.168.1.6:5000" 
#define SERVER_PORT 80 
int blueLED = 16;
int redLED = 17;
int yellowLED = 18;

DHT dht(DHT_PIN, DHT22);
void setup() {
  Serial.begin(115200);    
  pinMode(blueLED, OUTPUT);
  pinMode(redLED, OUTPUT);
  pinMode(yellowLED, OUTPUT);
  dht.begin();
  connectToWiFi();
}

void loop() {
  float  temp = dht.readTemperature();
  float hum = dht.readHumidity();
  Serial.println("Temp: " + String(temp, 2) + "°C");
  Serial.println("Humidity: " + String(hum, 1) + "%");

  if(temp >= 40){
    Serial.println("Panas");
    digitalWrite(redLED, HIGH);
    digitalWrite(blueLED, LOW);
    digitalWrite(yellowLED, LOW);
  }else if(temp >= 30){
    Serial.println("Hangat");
    digitalWrite(redLED, LOW);
    digitalWrite(blueLED, LOW);
    digitalWrite(yellowLED, HIGH);
  }else{
    Serial.println("Sejuk");
    digitalWrite(redLED, LOW);
    digitalWrite(blueLED, HIGH);
    digitalWrite(yellowLED, LOW);
  } Serial.println("-----------------------");

  HTTPClient http;
  String url = String(SERVER_ADDRESS) + "/route/sensor/data";
  JsonDocument jsonDoc; 

  jsonDoc["temp"] = temp;
  jsonDoc["hum"] = hum;
  jsonDoc["location"] = "Batu Sembilan";
  jsonDoc["id"] = "M0005";

  String postData;
  serializeJson(jsonDoc, postData);

  http.begin(url); 
  http.addHeader("Content-Type", "application/json");

  int httpResponseCode = http.POST(postData);

  if (httpResponseCode > 0) {
    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);
    String payload = http.getString();
    Serial.println(payload);
  } else {
    Serial.print("HTTP Error code: ");
    Serial.println(httpResponseCode);
  }Serial.println("-----------------------");

  http.end();
  delay(10000); 
}

void connectToWiFi() {
 Serial.println("Connecting to WiFi");
 WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

 while (WiFi.status() != WL_CONNECTED) {
   delay(1000);
   Serial.println("Connecting...");
 }
 
 Serial.println("Connected to WiFi");
}
