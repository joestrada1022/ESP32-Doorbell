# ESP32-CAM Doorbell Project

This project is designed to experiment with the ESP32-CAM module and learn the basics of wiring and IoT. The project includes the following components:

- **MQTT**: Used for messaging between the ESP32-CAM and the server.
- **Web Server**: A Flask-based server to handle photo uploads and display the interface.
- **Email Client**: Sends email notifications with attached photos when the doorbell button is pressed.
- **Embedded Programming**: Basic programming for the ESP32-CAM to capture and send images.

## Future Works
- add facial registering
- custom mobile app
- optimize methods

## Setup

1. **ESP32-CAM**: Flash the `doorbell_esp/doorbell_esp.ino` sketch to your ESP32-CAM module.
2. **Server**: Set up the Flask server by running `server/server.py`.
3. **Configuration**: Update the `config.h` file for the ESP32-CAM and the `.env` file for the server with your WiFi, MQTT, and email credentials.

## Usage

1. Press the doorbell button connected to the ESP32-CAM.
2. The ESP32-CAM captures an image and publishes it to the MQTT topic.
3. The server receives the image, sends an email notification
