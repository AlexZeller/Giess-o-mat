import MCP3008
import math
import sys
from time import sleep

class SoilMoisture:

    def __init__(self, mcp3008_channel):
        self.channel = mcp3008_channel

    def get_volumetric_water_content(self):
        adc = MCP3008.MCP3008()
        reading =adc.read_channel(self.channel)
        voltage = adc.convert_to_volts(reading, 4)
        vwc = ((1+16.103*voltage-(38.725*voltage)**2+(60.881*voltage)**3-(46.032*voltage)**4+(13.536*voltage)**5)-1.3)/6.1
        return round(vwc,4)

if __name__ == "__main__":

    try:
        channel = sys.argv[1]
        print('Reading converted volumetric soil moisture values of channel {}, press Ctrl-C to quit...'.format(channel))
    
        while True:
            soilmoisture = SoilMoisture(int(channel))
            moisture_reading = soilmoisture.get_volumetric_water_content()
            print('{0:>4} %'.format(moisture_reading))
            sleep(0.5)
    except KeyboardInterrupt:
        print('Stopped reading')