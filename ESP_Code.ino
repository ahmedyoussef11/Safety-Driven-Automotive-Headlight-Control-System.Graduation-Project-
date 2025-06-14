// Include necessary libraries
#include <WiFi.h>                  // For Wi-Fi connectivity
#include <PubSubClient.h>          // For MQTT communication
#include <Wire.h>                  // For I2C communication (used by magnetometer)
#include <Adafruit_Sensor.h>       // Adafruit sensor base class
#include <Adafruit_HMC5883_U.h>    // Adafruit driver for HMC5883L magnetometer

// ---------- Wi-Fi Configuration ----------
const char* ssid = "ahmed";                 // SSID of your Wi-Fi network
const char* password = "123456789";         // Password for your Wi-Fi network

// ---------- MQTT Configuration ----------
const char* mqtt_server = "192.168.50.1";   // IP address of MQTT broker (e.g., Raspberry Pi)
const int mqtt_port = 1883;                 // MQTT broker port (default is 1883)
const char* mqtt_client_id = "Car2";        // Unique ID for this ESP32 MQTT client
const char* topic_signal = "car2/signal";   // MQTT topic to publish RSSI (signal strength)
const char* topic_heading = "car/esp32_heading"; // MQTT topic to publish compass heading

WiFiClient espClient;               // Wi-Fi client for MQTT communication
PubSubClient client(espClient);     // MQTT client using the Wi-Fi connection

// ---------- Magnetometer Configuration ----------
Adafruit_HMC5883_Unified mag = Adafruit_HMC5883_Unified(12345); // Create magnetometer object with ID
float esp32_heading = 0;            // Variable to store the calculated compass heading

// ---------- Hardware Configuration ----------
const int LED_PIN = 2;              // GPIO2 (usually onboard LED on ESP32 boards)

// ---------- RSSI Sampling Configuration ----------
const int SAMPLE_INTERVAL = 100;    // Time between RSSI samples (in milliseconds)
const int NUM_SAMPLES = 5;          // Number of RSSI samples to average
int rssi_values[NUM_SAMPLES];       // Circular buffer to store recent RSSI samples

// ---------- Timing Variables ----------
unsigned long lastRSSISampleTime = 0; // Last time RSSI was sampled
int rssiSampleIndex = 0;              // Index to track current RSSI buffer slot

unsigned long lastHeadingTime = 0;           // Last time compass heading was sent
const unsigned long headingInterval = 100;   // Interval for heading updates (in milliseconds)

void setup() {
  Serial.begin(115200);             // Start serial communication for debugging
  pinMode(LED_PIN, OUTPUT);         // Set LED pin as output
  WiFi.setSleep(false);             // Disable Wi-Fi sleep to avoid interruptions

  WiFi.begin(ssid, password);       // Begin connecting to Wi-Fi network

  // Wait until connected to Wi-Fi
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);                    // Wait 1 second between connection attempts
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  client.setServer(mqtt_server, mqtt_port); // Set MQTT server and port
  reconnectMQTT();                // Connect to MQTT broker

  // Initialize the HMC5883L magnetometer
  if (!mag.begin()) {
    Serial.println("Couldn't find HMC5883L magnetometer!"); // Print error if not found
    while (1);  // Halt execution
  }
  Serial.println("HMC5883L found!"); // Successfully initialized magnetometer
}

void loop() {
  // If not connected to MQTT broker, reconnect
  if (!client.connected()) {
    digitalWrite(LED_PIN, LOW);    // Turn off LED if disconnected
    reconnectMQTT();               // Reconnect to MQTT broker
  } else {
    digitalWrite(LED_PIN, HIGH);   // Turn on LED if connected
  }

  client.loop();                   // Keep MQTT connection alive and handle incoming messages

  unsigned long now = millis();    // Get current time in milliseconds

  // ---------- Handle RSSI Sampling ----------
  if (now - lastRSSISampleTime >= SAMPLE_INTERVAL) {
    rssi_values[rssiSampleIndex] = WiFi.RSSI();  // Get current signal strength and store it
    rssiSampleIndex = (rssiSampleIndex + 1) % NUM_SAMPLES; // Move to next sample slot
    lastRSSISampleTime = now;      // Update last sample time

    // Calculate average RSSI
    float sum = 0;
    int valid = 0;
    for (int i = 0; i < NUM_SAMPLES; i++) {
      if (rssi_values[i] != 0) {   // Ignore uninitialized values (0)
        sum += rssi_values[i];     // Add to total sum
        valid++;                   // Count valid samples
      }
    }

    if (valid > 0) {
      float avg_rssi = sum / valid;  // Calculate average
      String payload = "{\"rssi\": " + String(avg_rssi, 2) + "}"; // Format as JSON
      client.publish(topic_signal, payload.c_str()); // Publish to MQTT
      Serial.println("Published RSSI: " + payload);  // Print to serial
    }
  }

  // ---------- Handle Heading Calculation ----------
  if (now - lastHeadingTime >= headingInterval) {
    lastHeadingTime = now;         // Update heading timer

    sensors_event_t event;
    mag.getEvent(&event);          // Read magnetometer data

    // Check if data is valid (non-zero)
    if (event.magnetic.x == 0 && event.magnetic.y == 0) {
      Serial.println("Invalid magnetometer data");
    } else {
      float heading = atan2(event.magnetic.y, event.magnetic.x); // Calculate heading in radians
      if (heading < 0) heading += 2 * PI;   // Convert negative to positive angle
      esp32_heading = degrees(heading);    // Convert to degrees

      String headingStr = String(esp32_heading);  // Convert to string
      client.publish(topic_heading, headingStr.c_str()); // Publish heading to MQTT
      Serial.print("Published Heading: ");
      Serial.println(headingStr + "°");   // Print heading to serial
    }
  }

  delay(5);  // Very short delay to avoid watchdog reset
}

// Function to reconnect to MQTT broker
void reconnectMQTT() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect(mqtt_client_id)) {
      Serial.println("connected");        // Successfully connected
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());       // Print error code
      Serial.println(" retrying in 5 sec");
      delay(5000);                        // Wait before retrying
    }
  }
}
