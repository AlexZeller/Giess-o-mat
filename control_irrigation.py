import time
from datetime import datetime, timedelta
from threading import Timer
import json
from giessomat import Relais, DC18B20, SoilMoisture

def read_json(path_json):
    """
    Takes a path to json file and returns json data as dictionary.

    Arguments:
        path_json (str): Path to json file.
    """

    with open(path_json) as s:
        settings = json.load(s)
    return(settings)


def irrig_soilMoisttime(soilMoist_min, start_time, interval, duration, 
                        channel=2, GPIO=25):
    """
    Irrigation is done for a certain duration in a certain interval if
    current soil moisture content is lower than soilMoist_min.

    Arguments:
        GPIO (int): GPIO pin used to switch Relais for pump and valve control.
        channel (int): Channel of ADC of SoilMoisture sensor.
        soilMoist_min (int): Minimum soil moisture accepted before irrigation starts.
        duration (int): Number in seconds indicating the duration of irrigation.
    """

    # Get current soil moisture reading
    soilmoisture = SoilMoisture.SoilMoisture(channel)
    moisture_reading = soilmoisture.get_volumetric_water_content()

    if moisture_reading <= soilH_min:
        print("Irrigation")
    else:
        print("No irrigation")


def irrig_soilMoist(soilMoist_min, duration, channel=2, GPIO=25):
    """
    Compares soilMoist_min with current soil moisture content. If statement
    is true irrigation starts.
    
    Arguments:
        GPIO (int): GPIO pin used to switch Relais for pump and valve control.
        channel (int): Channel of ADC of SoilMoisture sensor.
        soilMoist_min (int): Minimum soil moisture accepted before irrigation starts.
        duration (int): Number in seconds indicating the duration of irrigation.
    """

    soilmoisture = SoilMoisture.SoilMoisture(channel)
    moisture_reading = soilmoisture.get_volumetric_water_content()

    if moisture_reading <= soilH_min:
        irrigation.on()
        time.sleep(duration)
        irrigation.off()
    else:
        irrigation.off()

'''
def interval_execution(daydelta, start_hour, start_minute, function):
    
    now = datetime.today()
    nxt = now.replace(day=now.day, hour=start_hour, minute=start_minute, second=0, microsecond=0) + timedelta(days=daydelta)
    delta_t = nxt-now

    secs=delta_t.total_seconds()

    t = Timer(secs, function)
    t.start()
'''

def irrig_time(duration, GPIO=25):

    irrigation = Relais.Relais(GPIO)
    irrigation.on()
    time.sleep(duration)
    irrigation.off()


def interval_execution(mindelta, function):

    print("Interval execution started")
    now = datetime.today()
    nxt = now.replace(day=now.day, hour=now.hour, minute=now.minute, second=0, microsecond=0) + timedelta(minutes=mindelta)
    delta_t = nxt-now

    secs=delta_t.total_seconds()
    print("now", now)
    print("nxt", nxt)
    t = Timer(secs, function)
    t.start()

def test():
    print("Test is executed in a specific interval.")

if __name__ == '__main__':
    # Open JSON seetings file
    json_path = '/home/pi/Giess-o-mat-Webserver/irrigation_settings.json'
    irrigation_settings = read_json(json_path)

    interval_execution(2, test)

'''
    if irrigation_settings['auto'] == True:
        if irrigation_settings['mode'] == 'Zeit- und Bodenfeuchtesteuerung':
            print("Modus: Zeit- und Bodenfeuchtesteuerung")
            # Get settings
            start_hour = int(irrigation_settings['start_time'][0:2])
            start_minute = int(irrigation_settings['start_time'][3:5])
            soilMoist_min = int(irrigation_settings['soilMoist_min'])
            duration = int(irrigation_settings['duration'])
            interval = int(irrigation_settings['interval'])
            # Execute function
        elif irrigation_settings['mode'] == 'Zeitsteuerung':
            # Get settings
            start_hour = int(irrigation_settings['start_time'][0:2])
            start_minute = int(irrigation_settings['start_time'][3:5])
            duration = int(irrigation_settings['duration'])
            interval = int(irrigation_settings['interval'])
            # Execute function
        elif irrigation_settings['mode'] == 'Bodenfeuchtesteuerung':
            # Get settings
            soilMoist_min = int(irrigation_settings['soilMoist_min'])
            duration = int(irrigation_settings['duration'])
            # Execute function
            irrig_soilMoist(soilMoist_min, duration)
'''