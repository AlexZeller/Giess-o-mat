import datetime
import json
import sys
from giessomat import Relais, Photoresistor


def read_json(path_json, key):
    """
    Takes a path to json file and a key value and return all elements using this key.

    Arguments:
        path_json (str): Path to json file.
        key (str): Key for which all values will be returned.
    """

    with open(path_json) as s:
        settings = json.load(s)
    return(settings[key])

def light_time(start, end, GPIO=23):
    """
    Depending of the current time the light is switched on (start < current
    time < end )or off (start > current time, stop < current time).
    Arguments:
        start (int): Start time in minutes when lightning shall start.
        end (int): End time in minutes when lightning shall stop.
        GPIO (int): GPIO pin used to switch Relais for light control.
    """

    light = Relais.Relais(GPIO)
    current_time =  datetime.datetime.now().hour*60 + datetime.datetime.now().minute
    if start <= current_time and end >= current_time:
        light.on()
    else:
        light.off()


def light_time_sensor(start, end, lux_threshold, GPIO=23, channel=2):
    """
    Depending of the current time and the current lux_value the light is
    switched on (start < current time < end AND lux_value < lux threshold) or
    off (start > current time, stop < current time OR lux_value > lux_threshold).

    Arguments:
        start (int): Start time in minutes when lightning shall start.
        end (int): End time in minutes when lightning shall stop.
        lux_threshold (int): Minimum value excepted before additional light source is needed.
        GPIO (int): GPIO pin used to switch Relais for light control.
        channel (int): Channel of ADC.
    """

    light = Relais.Relais(GPIO)
    photoresistor = Photoresistor.Photoresistor(channel)
    # Get current lux value
    lux_reading = photoresistor.get_lux()
    
    current_time =  datetime.datetime.now().hour*60 + datetime.datetime.now().minute
    if lux_reading < lux_threshold and (start <= current_time and end >= current_time):
        light.on()
    else:
        light.off()


if __name__ == '__main__':
    # Open JSON seetings file
    json_path = '/home/pi/Giess-o-mat/user_settings.json'
    light_settings = read_json(json_path, 'light')

    # Write settinsg to variables
    if light_settings['auto'] == False:
        start_hour = light_settings['start_hour']
        start_minute = light_settings['start_min']
        end_hour = light_settings['end_hour']
        end_minute = light_settings['end_min']
        # Calculate start and end time in minutes
        start_time = int(start_hour)*60 + int(start_minute)
        end_time = int(end_hour)*60 + int(end_minute)
        print(start_time, end_time)
        if light_settings['mode'] == 'time_sensor_control':
            lux_threshold = light_settings['lux_threshold']
            # Call function for execution
            light_time_sensor(start_time, end_time, lux_threshold)
        else:
            # Call function for execution
            light_time(start_time, end_time)
