import RPi.GPIO as GPIO
import sys
import logging

# Set up logging
log = logging.getLogger(__name__)


class Relais:
    """ 
    Class to control one Relais Channel of a 4-Port Relais

    Attributes: 
        status (int): The status (on, off) of the Relais 
        gpio_pin (int): The number the connected GPIO Pin.        
    """

    def __init__(self, gpio_pin):
        """ 
        The constructor for the Relais class. 

        Arguments: 
            gpio_pin (int): The number the GPIO Pin to control the Relais.  
        """
        self.gpio_pin = gpio_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(gpio_pin, GPIO.OUT)

    def on(self):
        """ 
        Switches the Relais from NC to NO. 
        """

        GPIO.output(self.gpio_pin, GPIO.HIGH)
        self.status = True
        log.debug('Switched Relais on GPIO ' + str(self.gpio_pin) + ' on')

    def off(self):
        """ 
        Switches the Relais from NC to NO. 
        """

        GPIO.output(self.gpio_pin, GPIO.LOW)
        self.status = False
        log.debug('Switched Relais on GPIO ' + str(self.gpio_pin) + ' off')

    def get_status(self):
        """ 
        Get status of Relais. 
        """

        gpio_status = GPIO.input(self.gpio_pin)
        if gpio_status == 1:
            relais_status = True
        if gpio_status == 0:
            relais_status = False
        return relais_status


if __name__ == "__main__":
    try:
        gpio_pin = int(sys.argv[1])
        status = sys.argv[2]

        relais = Relais(gpio_pin)
        if status == 'on':
            relais.on()
            print('Switched Relais on pin {} from NC to NO'.format(gpio_pin))
        if status == 'off':
            relais.off()
            print('Switched Relais on pin {} from NO to NC'.format(gpio_pin))
    except:
        raise
