import sys
import sqlite3
from datetime import datetime

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
                                air_temp INTEGER,
                                air_humid INTEGER,
                                soil_temp INTEGER,
                                soil_humid INTEGER,
                                lux INTEGER,
                                waterlevel INTEGER
                                );"""
            self.cur.execute(create_table_sql)
        except sqlite3.Error as e:
            print(e)
        

    def executeSQL(self, *args):
        """
        Execution of a changeable number of SQL statements.

        Arguments:
            args (str): SQL statement. Multiple statements are possible 
                        (e.g. executeSQL(sql1, sql2,...))
        """

        for sql in args:
            self.cur.execute(sql)
        self.conn.commit()

if __name__ == "__main__":
    try:
        dbPath =  sys.argv[1] # Path to database
        sql = sys.argv[2] # SQL statement ("""INSERT INTO sensor_data2 VALUES (strftime("%s", CURRENT_TIME),5, 5, 5, 5, 5, 5)""")
        database = Database(dbPath)
        database.executeSQL(sql)
    except sqlite3.Error as e:
        print(e)