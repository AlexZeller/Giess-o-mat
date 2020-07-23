import time
from datetime import datetime, timedelta
import threading
from threading import Timer
import json
from giessomat import Relais, DC18B20, SoilMoisture, RepeatedTimer

def read_json(path_json):
    """
    Takes a path to json file and returns json data as dictionary.

    Arguments:
        path_json (str): Path to json file.
    """

    with open(path_json) as s:
        settings = json.load(s)
    return(settings)


def irrig_soilMoistTime(soilMoist_min, start_time, interval, duration, 
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

    irrigation = Relais.Relais(GPIO)

    if moisture_reading <= soilMoist_min:
        print("Irrigation")
        irrigation.on()
        time.sleep(duration)
        irrigation.off()
    else:
        print("No irrigation")
        irrigation.off()


def irrig_time(duration, GPIO=25):

    print("duration: ", duration)

    irrigation = Relais.Relais(GPIO)
    irrigation.on()
    time.sleep(duration)
    irrigation.off()


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

    irrigation = Relais.Relais(GPIO)

    if moisture_reading <= soilMoist_min:
        irrigation.on()
        time.sleep(duration)
        irrigation.off()
    else:
        irrigation.off()

def calcdelta(daydelta, time):
    """
    Calculates the remaining time in seconds from the current time to a specified other point in time.

    Arguments:
        daydelta (int): Day interval.
        time (str): Next point in time to which the time difference will be calculated (form: 'hh:mm').
    """
    # Get current time and set next time
    now = datetime.today()
    nxt = now.replace(day=now.day, hour=int(time[0:2]), minute=int(time[3:5]), second=0, microsecond=0) + timedelta(days=daydelta)
    # Calculate time difference
    delta_t = nxt-now
    secs=delta_t.total_seconds()

    return secs

# https://www.geeksforgeeks.org/python-different-ways-to-kill-a-thread/
if __name__ == '__main__':
    # Open JSON seetings file
    json_path = '/home/pi/Giess-o-mat-Webserver/irrigation_settings.json'
    irrigation_settings = read_json(json_path)

    if irrigation_settings['auto'] == True:
        if irrigation_settings['mode'] == 'Zeit- und Bodenfeuchtesteuerung':
            print("Modus: Zeit- und Bodenfeuchtesteuerung")
            # Get settings
            soilMoist_min = int(irrigation_settings['humidity_threshold'])
            duration = int(irrigation_settings['duration_irrigation'])
            interval = int(irrigation_settings['interval'])
            # Execute function
        elif irrigation_settings['mode'] == 'Zeitsteuerung':
            # Get settings
            duration = int(irrigation_settings['duration_irrigation'])
            interval = int(irrigation_settings['interval'])
            irrigation_number = int(irrigation_settings['number_irrigations'])
            print("Duration: ", duration)
            print("Interval: ", interval)
            if interval == 1:
                if irrigation_number == 1:
                    time_1 = irrigation_settings['irrigation_time_1']
                    delta_secs1 = calcdelta(interval, time_1)

                    print("Next execution at ", time_1)
                elif irrigation_number == 2:
                    time_1 = irrigation_settings['irrigation_time_1']
                    time_2 = irrigation_settings['irrigation_time_2']
                    # Calculate time delta
                    delta_secs1 = calcdelta(interval, time_1)
                    delta_secs2 = calcdelta(interval, time_2)

                    print("Next execution at ", time_1, " and ", time_2)
                    rt1 = RepeatedTimer.RepeatedTimer(delta_secs1, irrig_time, duration, GPIO=24)
                    rt1.start()
                    print("Thread 1: ", threading.enumerate())
                    rt2 = RepeatedTimer.RepeatedTimer(delta_secs2, irrig_time, duration, GPIO=24)
                    rt2.start()
                    print("Thread 2: ", threading.enumerate())
                elif irrigation_number == 3:
                    time_1 = irrigation_settings['irrigation_time_1']
                    time_2 = irrigation_settings['irrigation_time_2']
                    time_3 = irrigation_settings['irrigation_time_3']
                    # Calculate time delta
                    delta_secs1 = calcdelta(interval, time_1)
                    delta_secs2 = calcdelta(interval, time_2)
                    delta_secs3 = calcdelta(interval, time_3)

                    print("Next execution at ", time_1, ", ", time_2, " and ", time_3)
                
            else:
                time_1 = irrigation_settings['irrigation_time_1']
                delta_secs = calcdelta(interval, time_1)

                print("Next execution at ", time_1, " in ", delta_secs, " s")
                rt1 = RepeatedTimer.RepeatedTimer(delta_secs, irrig_time, duration, GPIO=24)
                print(rt1.is_running)
            #if not rt1.is_running:
            #    rt1.start()
        elif irrigation_settings['mode'] == 'Bodenfeuchtesteuerung':
            # Get settings
            soilMoist_min = int(irrigation_settings['humidity_threshold'])
            duration = int(irrigation_settings['duration_irrigation'])
            # Execute function
            irrig_soilMoist(soilMoist_min, duration)