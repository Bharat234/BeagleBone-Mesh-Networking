class Config:
    GPIO_CHIP = "/dev/gpiochip0"  # Check using `gpiodetect`
    IR_PIN = 14  # Change based on wiring
    BUZZER_PIN = 15
    LED_PIN = 16

    MQTT_BROKER = "192.168.0.101"  # Change to your MQTT broker’s IP
    MQTT_PORT = 1883
    MQTT_TOPIC_HIT = "laser_game/hit"
