from giessomat import Database
from giessomat import DHT22, HCSR04, DC18B20
#MCP3008, Photoresistor 

def get_sensordata(volume_cal_value, gpios_hcsr04 = [18, 12], gpio_dht22 = 17):
    """
    Reads all sensor values and returns it as a distionary.

    Arguments:
        gpio_dht22 (int):
        gpios_hcsr04 (arr): Array containing trigger (int) and echo (int) GPIO pin.
        volume_cal_value (int): Calibration value in cm which is equal to 1 % for volume calculation.
        photo_ch (int):
        soilmoist_ch (int):
        dc18b20_id (str)

    """
    # Sensor values from DHT22 (air temperature and humidity)
    dht22 = DHT22.DHT22(17)
    Ta = dht22.get_temperature()
    RH = dht22.get_humidity()
    
    # Sensor value from DC18B20(soil temperature)
    dc18b20 = DC18B20.DC18B20()
    soil_temp = dc18b20.get_temperature()
    
    # Sensor value from MCP3008 channel X (soil humidity)
    soil_humid = 9999

    # Sensor value from MCP3008 channel Y (lux)
    lux = 9999

    # Sensor value from HC-SR04 (water level)
    hcsr04 = HCSR04.HCSR04(gpios_hcsr04[0], gpios_hcsr04[1], volume_cal_value)
    waterlevel = hcsr04.calc_volume()

    return Ta, RH, soil_temp, soil_humid, lux, waterlevel


def sensordata2database(dbPath, sensordata):
    """
    Write sensor data to database.

    Arguments:
        dbPath (str): Path to database.
        sensordata (tuple): Order of the input values: Ta , RH, soil_temp, soil_humid, lux, waterlevel.
    """

    database = Database.Database(dbPath)
    sql = "INSERT INTO sensor_data VALUES (NULL, ?, ?, ?, ?, ?, ?);"
    database.executeSQL(sql, sensordata)


if __name__ == "__main__":
    try:
        sensordata = get_sensordata(volume_cal_value=1.73913)
        # sensordata: Ta, RH, soil_temp, soil_humid, lux, waterlevel
        sensordata2database('/home/pi/Giess-o-mat/giessomat_db.db', sensordata)
    except:
        pass
