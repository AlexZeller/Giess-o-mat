import datetime
import json
import sys
from giessomat import Relais, Photoresistor

# Load settings
#settings = json.loads('/home/pi/Giess-o-mat/user_settings.json')
#print('settings', settings)

# Set start and end time of lightning
start_hour = 6
start_minute = 0
end_hour = 22
end_minute = 00
# Calculate start and end time in minutes
start_time = int(start_hour)*60 + int(start_minute)
end_time = int(end_hour)*60 + int(end_minute)

def read_json(path_json, key):
    """
    EXPLANATION
    """
    with open(path_json, 'r+') as s:
        settings = json.load(s)
        print(settings[key])

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


def light_time_light(start, end, lux_threshold, GPIO=23, channel=2):
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
    json_path = sys.argv[1]
    read_json(json_path)
    #light_time(start_time, end_time)
