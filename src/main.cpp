/*
 * ESP32 Smart Lock System with Face Recognition
 * 
 * This code captures images from ESP32-CAM and sends them to the
 * Python face recognition server for authentication.
 */

#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <base64.h>
#include <ArduinoJson.h>

// WiFi Credentials
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// Face Recognition Server (Python server running on local network)
const char* serverUrl = "http://192.168.1.100:5000/recognize";  // Change to your server IP

// Lock Control Pin
#define LOCK_PIN 12  // GPIO pin for lock control (servo/relay)

// Button Pin (for manual capture)
#define BUTTON_PIN 13

// LED Indicators
#define LED_SUCCESS 14  // Green LED
#define LED_FAILURE 15  // Red LED

// Function declarations
void connectWiFi();
bool captureAndRecognize();
void unlockDoor();
void lockDoor();
String encodeImageToBase64(uint8_t* imageData, size_t length);

void setup() {
  Serial.begin(115200);
  delay(1000);
  
  Serial.println("\n=================================");
  Serial.println("ESP32 Smart Lock System");
  Serial.println("=================================");
  
  // Initialize pins
  pinMode(LOCK_PIN, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(LED_SUCCESS, OUTPUT);
  pinMode(LED_FAILURE, OUTPUT);
  
  // Initial state - locked
  lockDoor();
  digitalWrite(LED_SUCCESS, LOW);
  digitalWrite(LED_FAILURE, LOW);
  
  // Connect to WiFi
  connectWiFi();
  
  // TODO: Initialize camera module
  // Example for ESP32-CAM:
  // camera_config_t config;
  // config.pin_d0 = Y2_GPIO_NUM;
  // ... (configure camera pins)
  // esp_err_t err = esp_camera_init(&config);
  
  Serial.println("System ready!");
}

void loop() {
  // Check button press for manual capture
  if (digitalRead(BUTTON_PIN) == LOW) {
    delay(50);  // Debounce
    if (digitalRead(BUTTON_PIN) == LOW) {
      Serial.println("\nButton pressed - Starting face recognition...");
      
      bool recognized = captureAndRecognize();
      
      if (recognized) {
        Serial.println("✓ Access granted!");
        digitalWrite(LED_SUCCESS, HIGH);
        digitalWrite(LED_FAILURE, LOW);
        unlockDoor();
        delay(5000);  // Keep unlocked for 5 seconds
        lockDoor();
        digitalWrite(LED_SUCCESS, LOW);
      } else {
        Serial.println("✗ Access denied!");
        digitalWrite(LED_FAILURE, HIGH);
        digitalWrite(LED_SUCCESS, LOW);
        delay(2000);
        digitalWrite(LED_FAILURE, LOW);
      }
      
      // Wait for button release
      while(digitalRead(BUTTON_PIN) == LOW) {
        delay(10);
      }
    }
  }
  
  delay(100);
}

void connectWiFi() {
  Serial.print("Connecting to WiFi");
  WiFi.begin(ssid, password);
  
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    attempts++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n✓ WiFi connected");
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\n✗ WiFi connection failed!");
  }
}

bool captureAndRecognize() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("Error: WiFi not connected");
    return false;
  }
  
  // TODO: Replace this with actual camera capture
  // For now, we'll simulate with a placeholder
  /*
  camera_fb_t* fb = esp_camera_fb_get();
  if (!fb) {
    Serial.println("Error: Camera capture failed");
    return false;
  }
  
  // Encode image to base64
  String encodedImage = base64::encode(fb->buf, fb->len);
  esp_camera_fb_return(fb);
  */
  
  // Placeholder for testing (remove when camera is implemented)
  Serial.println("Note: Camera not implemented - add ESP32-CAM support");
  String encodedImage = "";  // This would be the actual base64 encoded image
  
  // Create JSON payload
  StaticJsonDocument<1024> jsonDoc;
  jsonDoc["image"] = encodedImage;
  
  String jsonPayload;
  serializeJson(jsonDoc, jsonPayload);
  
  // Send HTTP POST request
  HTTPClient http;
  http.begin(serverUrl);
  http.addHeader("Content-Type", "application/json");
  
  Serial.println("Sending request to server...");
  int httpCode = http.POST(jsonPayload);
  
  bool recognized = false;
  
  if (httpCode == 200) {
    String response = http.getString();
    Serial.println("Server response:");
    Serial.println(response);
    
    // Parse JSON response
    StaticJsonDocument<512> responseDoc;
    DeserializationError error = deserializeJson(responseDoc, response);
    
    if (!error) {
      bool success = responseDoc["success"];
      const char* name = responseDoc["name"];
      float confidence = responseDoc["confidence"];
      
      Serial.printf("Success: %s\n", success ? "true" : "false");
      Serial.printf("Name: %s\n", name);
      Serial.printf("Confidence: %.2f%%\n", confidence * 100);
      
      recognized = success;
    } else {
      Serial.println("Error parsing response");
    }
  } else {
    Serial.printf("HTTP Error: %d\n", httpCode);
    if (httpCode > 0) {
      Serial.println(http.getString());
    }
  }
  
  http.end();
  return recognized;
}

void unlockDoor() {
  Serial.println("→ Unlocking door");
  // TODO: Implement actual lock control
  // For servo: myservo.write(90);
  // For relay: digitalWrite(LOCK_PIN, HIGH);
  digitalWrite(LOCK_PIN, HIGH);
}

void lockDoor() {
  Serial.println("→ Locking door");
  // TODO: Implement actual lock control
  // For servo: myservo.write(0);
  // For relay: digitalWrite(LOCK_PIN, LOW);
  digitalWrite(LOCK_PIN, LOW);
}