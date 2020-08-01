import sys
import logging
import sqlite3
import Database
import DHT22
import HCSR04
import DC18B20
import MCP3008
import Photoresistor
import SoilMoisture

# Set up logging
log = logging.getLogger(__name__)


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
            create_sensor_table_sql = """CREATE TABLE IF NOT EXISTS sensor_data 
                                (timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                                air_temp REAL,
                                air_humid REAL,
                                soil_temp REAL,
                                soil_humid REAL,
                                lux REAL,
                                waterlevel REAL
                                );"""
                
            create_log_table_sql = """CREATE TABLE IF NOT EXISTS log 
                                (timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                                topic TEXT,
                                level TEXT,
                                message TEXT
                                );"""
            self.cur.execute(create_sensor_table_sql)
            self.cur.execute(create_log_table_sql)
            log.debug('Connected to database')
        except sqlite3.Error as e:
            log.exception('Error connecting to database')
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
        try:
            # Sensor values from DHT22 (air temperature and humidity)
            dht22 = DHT22.DHT22(17)
            Ta = dht22.get_temperature()
            RH = dht22.get_humidity()

            # Sensor value from DC18B20(soil temperature)
            dc18b20 = DC18B20.DC18B20()
            soil_temp = dc18b20.get_temperature()

            # Sensor value from MCP3008 channel X (soil humidity)
            soilmoisture = SoilMoisture.SoilMoisture(0)
            soil_humid = soilmoisture.get_volumetric_water_content()
           

            # Sensor value from MCP3008 channel Y (lux)
            photoresistor = Photoresistor.Photoresistor(7)
            lux = photoresistor.get_lux()

            # Sensor value from HC-SR04 (water level)
            hcsr04 = HCSR04.HCSR04(gpios_hcsr04[0], gpios_hcsr04[1])
            waterlevel = hcsr04.calc_volume()

            log.debug('Sucessfully read sensor values')
            return Ta, RH, soil_temp, soil_humid, lux, waterlevel
        except:
            log.exception('Error reading sensor values')

    def sensordata2database(self):
        """
        Write sensor data to database.
        """

        sensordata = self.get_sensordata()
        sql = "INSERT INTO sensor_data (air_temp, air_humid, soil_temp, soil_humid, lux, waterlevel) VALUES (?, ?, ?, ?, ?, ?);"
        try:
            self.executeSQL(sql, sensordata)
            log.info('Wrote sensor values to database')
        except:
            log.exception('Error writing sensor values to database')

    def log2database(self, topic, level, message):
        """
        Write log data to database.

        Arguments:
            topic (str): The topic of the log i.e irrigation
            level (str): The level of the message i.e error
            message (str): The message of the log
        """

        sql = "INSERT INTO log (topic, level, message) VALUES (?, ?, ?);"
        try:
            self.executeSQL(sql, (topic, level, message))
            log.debug('Wrote log to database')
        except:
            log.exception('Error writing log to database')


if __name__ == "__main__":
    try:
        db = Database('/home/pi/Giess-o-mat/giessomat_db.db')
        db.sensordata2database()
        #db.log2database('Ventilation', 'info', 'Nachtruhe. Fans off.')
    except:
        raise
