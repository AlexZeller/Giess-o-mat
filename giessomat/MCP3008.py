from spidev import SpiDev
from time import sleep
import sys

class MCP3008:
    """ 
    Class to read read the Channels of the MCP3008 Analog-to-Digital Converter

    Attributes: 
        bus (int): The number of the SPI bus that is used. 
        device (int): The number of the client device that is used.        
    """

    def __init__(self, bus = 0, device = 0):
        """ 
        The constructor for the MCP3008 class. 
          
        Arguments: 
            bus (int): The number of the SPI bus that is used. 
            device (int): The number of the client device that is used.   
        """

        self.bus, self.device = bus, device
        self.spi = SpiDev()
        self.spi.open(self.bus, self.device)
        # Necessary for Kernel 4.9 
        self.spi.max_speed_hz = 5000

    def read_channel(self, channel):
        """ 
        Read out the digital output of a channel. 
        
        Arguments: 
            channel (int): The channel to be read out.
        """

        adc = self.spi.xfer2([1, (8+channel)<<4, 0])   
        data = ((adc[1] & 3) << 8 ) + adc[2]
        return data

    def convert_to_volts(self, data, places):
        """ 
        Convert the digital output into a voltage. 
        
        Arguments: 
            data (int): The digital output of the channel reading.
            places (int): The number of decimal places.
        """

        volts = (data * 3.3) / float(1023)
        volts = round(volts,places)
        return volts

if __name__ == "__main__":

    try:
        channel = sys.argv[1]
        print('Reading MCP3008 values of channel {}, press Ctrl-C to quit...'.format(channel))
    
        while True:
            adc = MCP3008()
            value = adc.convert_to_volts(int(adc.read_channel(int(channel))),4)
            print('{0:>4}V'.format(value))
            sleep(0.5)
    except KeyboardInterrupt:
        print('Stopped reading')
