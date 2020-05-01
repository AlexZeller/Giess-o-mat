import sys
import RPi.GPIO as GPIO
import time
import math

class HC-SR04:
    """
    Class to read the sensor values (ultrasonic) from HC-SR04.

    Attributes:
        gpio_trigger (int): Number of GPIO Pin which triggers the ultrasonic signal.
        gpio_echo (int): Number of GPIO Pin which receives the ultrasonic signal.
    """

    def __init__(self, gpio_trigger, gpio_echo):
        """
        The constructor for the HC-SR04 class.
        
        Arguments:
            gpio_trigger (int): Number of GPIO Pin which triggers the ultrasonic signal.
            gpio_echo (int): Number of GPIO Pin which receives the ultrasonic signal.
        """

        self.gpio_trigger = gpio_trigger
        self.gpio_echo = gpio_echo

        #GPIO Modus (BOARD / BCM)
        GPIO.setmode(GPIO.BCM)

        #Set directions of GPIO-Pins (IN / OUT)
        GPIO.setup(gpio_trigger, GPIO.OUT)
        GPIO.setup(gpio_echo, GPIO.IN)

    def get_distance(self):
        """
        Calculates the distance to the next object based on time difference
        between sender and receiver.
        """

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

if __name__ == "__main__":
    try:
        gpio_trigger = sys.argv[1]
        gpio_echo = sys.argv[2]

        hc-sr04 = HC-SR04(gpio_trigger, gpio_echo)
        print('Distance: ', hc-sr04.get_distance())
    except:
        print('Something did not work with HC-SR04.')