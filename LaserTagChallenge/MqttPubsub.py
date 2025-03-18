import Adafruit_BBIO.GPIO as GPIO
import time
import threading
import paho.mqtt.client as mqtt
import os

# Define GPIO pins on P9
IR_LED_PIN = "LED_GPIO_PIN"     # Used for both IR transmission and visual feedback
IR_SENSOR_PIN = "IR_GPIO_PIN"  # IR sensor for detecting incoming signals
BUZZER_PIN = "BUZZER_GPIO_PIN"     # Buzzer for game-over indication

# Setup pins: IR LED and Buzzer as outputs; IR Sensor as input
GPIO.setup(IR_LED_PIN, GPIO.OUT)
GPIO.setup(IR_SENSOR_PIN, GPIO.IN)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

# MQTT Setup
BROKER = "BROKER_IP"  # Replace with your MQTT broker's IP address
TOPIC = "laser_tag/shoot"
PLAYER_ID = input("Enter your Player ID: ")  # Unique ID for each BBB

client = mqtt.Client()
client.connect(BROKER, 1883, 60)
client.subscribe(TOPIC)

# Initialize player HP (health points)
local_hp = 10 # Can change according to requirements

# Dictionary to track all players' HP; use a lock for thread safety
players = {}
players_lock = threading.Lock()

# At startup, add self to players dictionary and publish join message
with players_lock:
    players[PLAYER_ID] = local_hp
client.publish(TOPIC, f"{PLAYER_ID}:Join:{local_hp}")

# Function to check if a winner exists among all players
def check_for_winner():
    with players_lock:
        total_players = len(players)
        alive = [pid for pid, hp_val in players.items() if hp_val > 0]
    # Only check for a winner if more than one player is connected.
    if total_players > 1 and len(alive) == 1:
        winner = alive[0]
        print(f"🏆 Winner is {winner}!")
        client.publish(TOPIC, f"Winner:{winner}:0")
        time.sleep(1)
        client.disconnect()
        os._exit(0)

# Function to simulate shooting via IR LED pulses and visual LED flash
def shoot_ir():
    print(f"🔥 {PLAYER_ID} shooting!")
    client.publish(TOPIC, f"{PLAYER_ID}:Fired")
    
    # Flash LED to indicate firing (visual feedback)
    GPIO.output(IR_LED_PIN, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(IR_LED_PIN, GPIO.LOW)
    
    # Optionally, also send a series of IR pulses
    for _ in range(10):
        GPIO.output(IR_LED_PIN, GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(IR_LED_PIN, GPIO.LOW)
        time.sleep(0.001)

# Function to detect hits using the IR sensor, update HP, and control buzzer/LED
def detect_hits():
    global local_hp
    print("👀 Listening for IR hits...")
    while True:
        # Many IR receiver modules are active low (0 indicates detection)
        if GPIO.input(IR_SENSOR_PIN) == 0:
            print("💥 HIT DETECTED!")
            # Flash LED briefly on hit
            GPIO.output(IR_LED_PIN, GPIO.HIGH)
            time.sleep(0.1)
            GPIO.output(IR_LED_PIN, GPIO.LOW)
            
            # Update local HP in a thread-safe way
            with players_lock:
                if local_hp > 0:
                    local_hp -= 1
                    players[PLAYER_ID] = local_hp
                    print(f"Player {PLAYER_ID} HP: {local_hp}")
            # Publish updated HP message
            if local_hp > 0:
                client.publish(TOPIC, f"{PLAYER_ID}:HP:{local_hp}")
            else:
                # Local player HP reached 0: publish GameOver, buzz for 10 seconds, and exit.
                print("HP is zero! Game Over. Activating buzzer!")
                client.publish(TOPIC, f"{PLAYER_ID}:GameOver:0")
                GPIO.output(BUZZER_PIN, GPIO.HIGH)
                time.sleep(2)
                GPIO.output(BUZZER_PIN, GPIO.LOW)
                client.disconnect()
                os._exit(0)
            time.sleep(1)  # Debounce delay
            check_for_winner()

# MQTT message handler to process incoming events from other players
def on_message(client, userdata, msg):
    global players
    try:
        message = msg.payload.decode()
        parts = message.split(":")
        if len(parts) < 2:
            return
        sender_id = parts[0]
        action = parts[1]
        
        # Ignore messages from self (except join to update our local players list)
        if sender_id == PLAYER_ID and action != "Join":
            return
        
        if action == "Join":
            # New player joining: update dictionary
            hp_val = int(parts[2]) if len(parts) > 2 else 10
            with players_lock:
                players[sender_id] = hp_val
            print(f"📥 {sender_id} joined with HP {hp_val}")
        elif action == "Fired":
            print(f"🔥 {sender_id} fired!")
        elif action == "HP":
            hp_val = int(parts[2])
            with players_lock:
                players[sender_id] = hp_val
            print(f"⚠ {sender_id} HP updated to {hp_val}")
        elif action == "GameOver":
            with players_lock:
                players[sender_id] = 0
            print(f"💀 {sender_id} is out of the game!")
        elif action == "Winner":
            winner = sender_id  # or parts[1] could be used if different format
            print(f"🏆 {winner} has been declared the winner!")
            client.disconnect()
            os._exit(0)
        
        check_for_winner()
    except Exception as e:
        print("Error processing message:", e)

client.on_message = on_message

# Start the MQTT client loop in a background thread
threading.Thread(target=lambda: client.loop_forever(), daemon=True).start()

# Start IR sensor hit detection in a background thread
threading.Thread(target=detect_hits, daemon=True).start()

# Main loop for shooting commands
try:
    while True:
        command = input("Press ENTER to shoot, or type 'exit' to quit: ")
        if command.lower() == "exit":
            break
        shoot_ir()
except KeyboardInterrupt:
    pass

client.disconnect()
GPIO.cleanup()
