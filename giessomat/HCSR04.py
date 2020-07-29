import sys
import RPi.GPIO as GPIO
import time
import math
import logging

# Set up logging
log = logging.getLogger(__name__)


class HCSR04:
    """
    Class to read the sensor values (ultrasonic) from HC-SR04.

    Attributes:
        gpio_trigger (int): Number of GPIO Pin which triggers the ultrasonic signal.
        gpio_echo (int): Number of GPIO Pin which receives the ultrasonic signal.
    """

    def __init__(self, gpio_trigger, gpio_echo, val0p=62, val1d=1.78571428571):
        """
        The constructor for the HC-SR04 class.

        Arguments:
            gpio_trigger (int): Number of GPIO Pin which triggers the ultrasonic signal.
            gpio_echo (int): Number of GPIO Pin which receives the ultrasonic signal.
            val0p (int): Calibration value in cm which is equal to 0 %.
                pipe solution: 56.5 cm equals 1 %
                box solution: X cm equals 1 %.
            val1d (int): Calibration value in percent which equals 1 cm.
                pipe solution: 1 cm equals 2 %
                box solution: 1 equals X %
        """

        self.gpio_trigger = gpio_trigger
        self.gpio_echo = gpio_echo
        self.val0p = val0p
        self.val1d = val1d

        # GPIO Modus (BOARD / BCM)
        GPIO.setmode(GPIO.BCM)

        # Set directions of GPIO-Pins (IN / OUT)
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

        log.debug('Calculated distance')
        return distance
    
    def calc_volume(self):
        """
        Returns the left volume in the container in percent.
        """
        distance = self.get_distance()
        p = round((self.val0p - distance)*self.val1d, 2)
        log.debug('Calculated volume')
        return p


if __name__ == "__main__":
    try:
        gpio_trigger = sys.argv[1]
        gpio_echo = sys.argv[2]
        cal_value = sys.argv[3]

        hc_sr04 = HCSR04(int(gpio_trigger), int(gpio_echo), float(cal_value))
        dist = hc_sr04.get_distance()
        vol = hc_sr04.calc_volume()
        print('Distance: ', dist)
        print('Volume left: ', vol)
    except:
        raise
        print('Something did not work with HC-SR04.')
