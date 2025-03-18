# BBB Laser Tag Game

This project is a multiplayer laser tag game built with multiple BeagleBone Black (BBB) boards connected over a mesh network using MQTT for communication. Each BBB acts as a player that can:

- **Fire:** Use an IR LED to shoot. Visual feedback is provided by flashing the IR LED.
- **Detect Hits:** An IR sensor detects incoming IR signals (representing hits), and a buzzer sounds when a player’s health (HP) reaches zero.
- **Synchronize:** MQTT messages are used to share game events (fire, hit, HP update, game over, winner) across all devices.
- **Determine Winner:** When a player’s HP drops to zero, a buzzer is activated for 10 seconds and then the player exits. The game continuously checks for the last player standing and declares them the winner.

## Features

- Multiplayer gameplay using a mesh network.
- Real-time game status sharing via MQTT.
- HP tracking and automatic winner determination.
- Visual (LED) and audio (buzzer) feedback for game events.

## Hardware Setup

### Components

- **BeagleBone Black** (one per player)
- **IR LED** (for firing and visual feedback)
- **IR Sensor** (for detecting hits)
- **Buzzer** (for game-over signal)
- **Resistors** (e.g., 220Ω for LED current limiting) (optional)
- **Breadboard and Jumper wires**

### Wiring (Example on P9 Header)

- **IR LED:**  
  - Anode (with resistor) → P9_11  
  - Cathode → Ground (GND)
  
- **IR Sensor:**  
  - Signal out → P9_12  
  - Vcc and GND as required (check your sensor’s datasheet)
  
- **Buzzer:**  
  - Positive → P9_13  
  - Negative → Ground (GND)

> **Note:** Verify your component’s specifications. Many IR LEDs emit in the invisible IR range. For testing the IR LED, a digital camera may help you see the light.

## Software Setup

### Prerequisites

- A running instance of an MQTT Broker (e.g., Mosquitto) on your network.  
- Python 3 installed on your BBB.
- The BeagleBone running Debian (or a compatible distribution).

### Installation

1. Clone or download the project files.
2. Install the required Python packages using the provided `requirements.txt` file:
   ```bash
   pip3 install -r requirements.txt
