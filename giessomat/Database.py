import sys
import sqlite3
#from datetime import datetime

class Database:
    """
    Class to connect to database and execute SQL statements.

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

if __name__ == "__main__":
    try:
        dbPath =  sys.argv[1] # Path to database: '/home/pi/Giess-o-mat/giessomat_db.db'
        sql = sys.argv[2] # SQL statement ("""INSERT INTO sensor_data VALUES (NULL, 9999, 9999, 9999, 9999, 9999, 9999)""")
        database = Database(dbPath)
        database.executeSQL(sql)
    except sqlite3.Error as e:
        print(e)