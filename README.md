# V2V Communication System

The Vehicle-to-Vehicle (V2V) communication system developed in this project enables real-time data exchange between nearby vehicles to enhance driving safety and coordination. Our system uses ESP32 microcontrollers, GY-87 IMU modules, and the GY-271 magnetometer to detect and share each vehicle's heading and orientation. Communication is handled through the lightweight MQTT protocol, allowing vehicles to determine whether they are approaching each other and to trigger automatic actions such as headlight dimming to prevent glare. This low-cost, reliable solution simulates how modern connected vehicles exchange data to support intelligent decision-making in dynamic driving environments.

![141950897](https://github.com/user-attachments/assets/c1946a7d-35af-424b-bb84-fd1150b4598c)

---

## Why We Used MQTT

For our V2V communication system, we selected MQTT (Message Queuing Telemetry Transport) due to its lightweight design, low bandwidth usage, and real-time messaging capabilities. MQTT is ideal for embedded systems like the ESP32, where efficient and reliable communication is essential. Unlike heavier protocols, MQTT uses a publish/subscribe model that allows vehicles to exchange only the necessary data — such as heading and orientation — with minimal delay. This ensures that our system can react instantly to approaching vehicles, making it a practical and scalable solution for real-world automotive communication.

![Screenshot_2025-06-11_010830-removebg-preview](https://github.com/user-attachments/assets/d3349f5c-0b2c-4ec9-82ad-9d4f74b77f0e)

---

## Role of GY Sensors in the Project

In our V2V communication system, we used the GY-271 HMC5883L magnetometer to accurately measure each vehicle's heading (compass direction). This sensor detects the Earth's magnetic field across three axes, allowing us to determine the real-time orientation of a vehicle.

By integrating the GY-271 with the ESP32, each vehicle continuously calculates its heading and publishes it via MQTT. When another vehicle receives this data, it compares it with its own heading to determine whether both are moving toward each other. If so, the system triggers an automatic adjustment in headlight brightness to prevent glare.

The GY-271 was chosen for its precision, low power consumption, compact design, and compatibility with microcontrollers, making it an ideal fit for embedded automotive applications. It plays a critical role in enabling direction-based decision-making without relying on GPS, ensuring fast and localized responses for enhanced road safety.


