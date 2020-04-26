import RPi.GPIO as GPIO
import time
import math

class Distanz:
    def __init__(self, gpio_trigger, gpio_echo):
        self.gpio_trigger = gpio_trigger
        self.gpio_echo = gpio_echo

        #GPIO Modus (BOARD / BCM)
        GPIO.setmode(GPIO.BCM)

        #Set directions of GPIO-Pins (IN / OUT)
        GPIO.setup(gpio_trigger, GPIO.OUT)
        GPIO.setup(gpio_echo, GPIO.IN)

    def get_distanz(self):
        # Set trigger to HIGH
        GPIO.output(self.gpio_trigger, True)
    
        # Set trigger to LOW after 0.01ms
        time.sleep(0.00001)
        GPIO.output(self.gpio_trigger, False)
    
        starttime = time.time()
        endtime = time.time()
    
        # Save starttime
        while GPIO.input(self.gpio_echo) == 0:
            starttime = time.time()
    
        # Save endtime
        while GPIO.input(self.gpio_echo) == 1:
            endtime = time.time()
    
        # Time difference between start and end
        TimeElapsed = endtime - starttime
        # multiply with sonic speed (34300 cm/s) and divide by two (there and back)
        distance = (TimeElapsed * 34300) / 2
    
        return distance