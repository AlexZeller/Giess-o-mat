import os
import sys

class DC18B20:
    """
    Class to read the sensor values from DC18B20 (soil temperature).

    Attributes:
        sensor_id (str): Id of the sensor.  
    """

    def __init__(self, sensor_id = '28-0301a27973a0'):
        """
        The constructor for the DC18B20 class.
        
        Arguments:
            sensor_id (str): Id of the sensor.
        """

        self.sensor_id = sensor_id


    def get_temperature(self):
        """
        Reads the temperature value from the sensor and returns it.
        """

        # Read 1-wire slave data
        file = open('/sys/bus/w1/devices/{}/w1_slave'.format(self.sensor_id))
        filecontent = file.read()
        file.close()

        # Read temperature values and convert it to degree Celsius
        stringvalue = filecontent.split('\n')[1].split(' ')[9]
        temperature = float(stringvalue[2:]) / 1000
        temperature = '%6.2f' % temperature
        return(temperature)


if __name__ == "__main__":
    try:
        dc18b20 = DC18B20()
        soil_temp = dc18b20.get_temperature()
        print(soil_temp)
    except:
        pass