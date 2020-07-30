import MCP3008
import math
import sys
from time import sleep
import logging

# Set up logging
log = logging.getLogger(__name__)

class Photoresistor:

    def __init__(self, mcp3008_channel):
        self.channel = mcp3008_channel

    def get_lux(self):
        adc = MCP3008.MCP3008()
        try:
            reading =adc.read_channel(self.channel)
            voltage = adc.convert_to_volts(reading, 4)
            lux = 322*voltage**2+719*voltage+187
            log.debug('Converted MCP3008 reading to LUX')
            return int(lux)
        except:
            log.error('Error getting reading LUX reading')

if __name__ == "__main__":

    try:
        channel = sys.argv[1]
        print('Reading converted Lux values of Photoresistor of channel {}, press Ctrl-C to quit...'.format(channel))
    
        while True:
            photoresistor = Photoresistor(int(channel))
            lux_reading = photoresistor.get_lux()
            if lux_reading > 5000:
		print('>5000 Lux')            
	    else:
		print('{0:>4} Lux'.format(lux_reading))
            sleep(0.5)
    except KeyboardInterrupt:
        print('Stopped reading')
