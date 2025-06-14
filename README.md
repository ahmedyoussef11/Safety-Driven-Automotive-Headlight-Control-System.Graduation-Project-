# V2V Communication System

The Vehicle-to-Vehicle (V2V) communication system developed in this project enables real-time data exchange between nearby vehicles to enhance driving safety and coordination. Our system uses ESP32 microcontrollers, GY-87 IMU modules, and the GY-271 magnetometer to detect and share each vehicle's heading and orientation. Communication is handled through the lightweight MQTT protocol, allowing vehicles to determine whether they are approaching each other and to trigger automatic actions such as headlight dimming to prevent glare. This low-cost, reliable solution simulates how modern connected vehicles exchange data to support intelligent decision-making in dynamic driving environments.

![141950897](https://github.com/user-attachments/assets/c1946a7d-35af-424b-bb84-fd1150b4598c)


## Why We Used MQTT

For our V2V communication system, we selected MQTT (Message Queuing Telemetry Transport) due to its lightweight design, low bandwidth usage, and real-time messaging capabilities. MQTT is ideal for embedded systems like the ESP32, where efficient and reliable communication is essential. Unlike heavier protocols, MQTT uses a publish/subscribe model that allows vehicles to exchange only the necessary data — such as heading and orientation — with minimal delay. This ensures that our system can react instantly to approaching vehicles, making it a practical and scalable solution for real-world automotive communication.

![mqtt-logo-ver-removebg-preview](https://github.com/user-attachments/assets/1f54724a-bfb0-4bf7-8f34-ccd3f8603e4f)
