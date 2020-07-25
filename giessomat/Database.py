import sys
import sqlite3
import Database
import DHT22
import HCSR04
import DC18B20
import MCP3008
import Photoresistor


class Database:
    """
    Class to connect to database, execute SQL statements and write sensordata to 
    Database.

    Attributes:
        dbPath (str): Path to database.
    """

    def __init__(self, dbPath):
        """
        Initializes the database at given location and provides database connection.
        If 'sensor_data' table does not already exist it is created.

        Arguments:
            dbPath (str): Path to database.
        """

        self.dbPath = dbPath
        # Initialize database if not already exist
        try:
            # Create connection object
            self.conn = sqlite3.connect(dbPath)
            # Create cursor object
            self.cur = self.conn.cursor()

            # Create table if not already exist
            create_table_sql = """CREATE TABLE IF NOT EXISTS sensor_data 
                                (timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                                air_temp REAL,
                                air_humid REAL,
                                soil_temp REAL,
                                soil_humid REAL,
                                lux REAL,
                                waterlevel REAL
                                );"""
            self.cur.execute(create_table_sql)
        except sqlite3.Error as e:
            print(e)

    def executeSQL(self, sql, par):
        """
        Execution of a changeable number of SQL statements.

        Arguments:
            sql (str): SQL statement.
            par (tuple): Variables which shall be inserted in SQL statement.
        """

        self.cur.execute(sql, par)
        self.conn.commit()

    def get_sensordata(self, gpios_hcsr04=[18, 12], gpio_dht22=17):
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
        hcsr04 = HCSR04.HCSR04(gpios_hcsr04[0], gpios_hcsr04[1])
        waterlevel = hcsr04.calc_volume()

        return Ta, RH, soil_temp, soil_humid, lux, waterlevel

    def sensordata2database(self):
        """
        Write sensor data to database.
        """

        sensordata = self.get_sensordata()
        sql = "INSERT INTO sensor_data (air_temp, air_humid, soil_temp, soil_humid, lux, waterlevel) VALUES (?, ?, ?, ?, ?, ?);"
        self.executeSQL(sql, sensordata)


if __name__ == "__main__":
    try:
        db = Database('/home/pi/Giess-o-mat/giessomat_db.db')
        db.sensordata2database()
    except:
        raise
