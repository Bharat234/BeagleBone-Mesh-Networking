import gpiod
import time

class IRSensor:
    def __init__(self, chip_name, pin):
        self.chip = gpiod.Chip(chip_name)
        self.line = self.chip.get_line(pin)
        self.line.request(consumer="laser_tag", type=gpiod.LINE_REQ_DIR_IN, flags=[gpiod.LINE_REQ_FLAG_BIAS_PULL_UP])

    def detect_hit(self):
        return self.line.get_value() == 0  # Active-low signal

class BuzzerLED:
    def __init__(self, chip_name, buzzer_pin, led_pin):
        self.chip = gpiod.Chip(chip_name)
        self.buzzer = self.chip.get_line(buzzer_pin)
        self.led = self.chip.get_line(led_pin)
        self.buzzer.request(consumer="laser_tag", type=gpiod.LINE_REQ_DIR_OUT)
        self.led.request(consumer="laser_tag", type=gpiod.LINE_REQ_DIR_OUT)

    def trigger_feedback(self):
        self.buzzer.set_value(1)
        self.led.set_value(1)
        time.sleep(0.2)
        self.buzzer.set_value(0)
        self.led.set_value(0)
