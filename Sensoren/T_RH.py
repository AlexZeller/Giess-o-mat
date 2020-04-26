import Adafruit_DHT

class T_RH:
    def __init__(self, gpio_pin):
        self.gpio_pin = gpio_pin
        self.dht_type = Adafruit_DHT.DHT22

    def get_temperature(self):
        values = Adafruit_DHT.read_retry(self.dht_type, self.gpio_pin)
        temperature = round(values[1], 1)
        return temperature

    def get_humidity(self):
        values = Adafruit_DHT.read_retry(self.dht_type, self.gpio_pin)
        humidity = round(values[0], 1)
        return humidity