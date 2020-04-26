import sys
import RPi.GPIO as GPIO

class Relais:
    def __init__(self, gpio_pin):
        self.gpio_pin = gpio_pin
        self.status = None
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(gpio_pin, GPIO.OUT)

    def on(self):
        GPIO.output(self.gpio_pin, GPIO.LOW)
        self.status = "on" 

    def off(self):
        GPIO.output(self.gpio_pin, GPIO.HIGH) 
        self.status = "off"