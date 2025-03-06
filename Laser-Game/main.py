import time
import paho.mqtt.client as mqtt
from hardware import IRSensor, BuzzerLED
from config import Config

# Initialize components
ir_sensor = IRSensor(Config.GPIO_CHIP, Config.IR_PIN)
buzzer_led = BuzzerLED(Config.GPIO_CHIP, Config.BUZZER_PIN, Config.LED_PIN)

# Setup MQTT client
mqtt_client = mqtt.Client()
mqtt_client.connect(Config.MQTT_BROKER, Config.MQTT_PORT, 60)

HP = 3  # Player starts with 3 lives

print("Game Ready! Waiting for shots...")

try:
    while HP > 0:
        if ir_sensor.detect_hit():
            HP -= 1
            print(f"Hit detected! HP left: {HP}")
            mqtt_client.publish(Config.MQTT_TOPIC_HIT, f"Player hit! HP: {HP}")
            buzzer_led.trigger_feedback()
            if HP == 0:
                print("You're out!")
                mqtt_client.publish(Config.MQTT_TOPIC_HIT, "Player eliminated!")
                break
            time.sleep(0.5)  # Prevent multiple detections from one hit
except KeyboardInterrupt:
    print("Exiting...")
    mqtt_client.disconnect()
