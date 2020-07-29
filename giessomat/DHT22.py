import sys
import Adafruit_DHT
import logging

# Set up logging
log = logging.getLogger(__name__)

class DHT22:
    """
    Class to read the sensor values (air temperature and humidity) from DHT22.

    Attributes:
        gpio_pin (int): The number the GPIO Pin to control the DHT22.
        dht_type (int): Type of the DHT sensor.
    """

    def __init__(self, gpio_pin=17):
        """
        The constructor for the DHT22 class.
        
        Arguments:
            gpio_pin (int): The number the GPIO Pin to control the DHT22.
        """

        self.gpio_pin = gpio_pin
        self.dht_type = Adafruit_DHT.DHT22

    def get_temperature(self):
        """ 
        Reads the temperature value from the sensor and returns it.
        """
        try:
            values = Adafruit_DHT.read_retry(self.dht_type, self.gpio_pin)
            log.debug('Read DHT22 temperature value')
            temperature = round(values[1], 2)
            return temperature
        except:
            log.error('Failed to read DHT22 temperature value')


    def get_humidity(self):
        """
        Reads the humdity value from the sensor and returns it.
        """
        try:
            values = Adafruit_DHT.read_retry(self.dht_type, self.gpio_pin)
            log.debug('Read DHT22 humidity value')
            humidity = round(values[0], 2)
            return humidity
        except:
            log.error('Failed to read DHT22 humidity value')


if __name__ == "__main__":
    try:
        gpio_pin = sys.argv[1]
        dht22 = DHT22(gpio_pin)
        print('Air temperature: ', dht22.get_temperature())
        print('Humidity: ', dht22.get_humidity())
    except:
        raise
        print('Something did not work with DHT22.')