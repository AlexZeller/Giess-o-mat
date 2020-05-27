import datetime
import json
import sys
from giessomat import Relais, Photoresistor


def read_json(path_json):
    """
    Takes a path to json file and returns json data as dictionary.

    Arguments:
        path_json (str): Path to json file.
    """

    with open(path_json) as s:
        settings = json.load(s)
    return(settings)

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
    json_path = '/home/pi/Giess-o-mat-Webserver/light_settings.json'
    light_settings = read_json(json_path)

    # Write settinsg to variables
    if light_settings['auto'] == True:
        start_hour = int(light_settings['start_time'][0:2])
        start_minute = int(light_settings['start_time'][3:5])
        end_hour = int(light_settings['end_time'][0:2])
        end_minute = int(light_settings['end_time'][3:5])
        
        # Calculate start and end time in minutes
        start_time = start_hour*60 + start_minute
        end_time = end_hour*60 + end_minute

        if light_settings['mode'] == 'Zeit- und Helligkeitssteuerung':
            lux_threshold = light_settings['lux_threshold']
            # Call function for execution
            light_time_sensor(start_time, end_time, lux_threshold)
        elif light_settings['mode'] == 'Zeitsteuerung'::
            # Call function for execution
            light_time(start_time, end_time)
    else:
        print("XXX")
