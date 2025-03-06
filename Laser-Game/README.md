# BeagleBone Black Laser Tag Game

## Overview
This project implements a simple laser tag game using BeagleBone Black (BBB). It utilizes IR sensors to detect hits, buzzers and LEDs for feedback, and MQTT for communication between devices.

## Hardware Requirements
- BeagleBone Black (4 units for multiplayer setup)
- IR Receiver
- IR Transmitter (Laser gun)
- Buzzer
- LED
- Ethernet switch (for networking)

## Software Requirements
- Python 3
- `gpiod` for GPIO control
- `paho-mqtt` for MQTT messaging

## Installation
1. Install dependencies:
   ```sh
   pip install -r requirements.txt
