import datetime
from giessomat import Relais, DHT22


def read_json(path_json):
    """
    Takes a path to json file and returns json data as dictionary.

    Arguments:
        path_json (str): Path to json file.
    """

    with open(path_json) as s:
        settings = json.load(s)
    return(settings)


def vent_at_times(times, GPIO=24):
    """
    Ventilation is executed at specific times.
    
    Arguments:
        times (array): Each time in times is a 2D Array 
            time (array): [start_hour (int), start_min (int)]
        GPIO (int): GPIO pin used to switch Relais for ventilation control.
    """

    ventilation = Relais.Relais(GPIO)
    # Get current time
    current_time =  datetime.datetime.now().hour*60 + datetime.datetime.now().minute
    # Compare time with current time 
    for time in times:
        tmp = time[0]*60 + time[1]
        time_delta = tmp - current_time
        if time_delta <= 0 and time_delta > -10:
            ventilation.on()
            break
        else:
            ventilation.off()


def vent_TaRH(Ta, RH, Ta_max, RH_max, GPIO=24):
    """
    Compares Ta with Ta_max and RH with RH_max. If statement is true/false
    ventilation starts/stops.
    
    Arguments:
        Ta (float): Actual air temperature measured with DHT22.
        RH (float): Actual humidity measured with DHT22.
        Ta_max (int): Maximum air temperature accepted before ventialtion starts.
        RH_max (int): Maximum humidity (in percent) accepted before ventilation starts.
        GPIO (int): GPIO pin used to switch Relais for ventilation control.
    """

    ventilation = Relais.Relais(GPIO)
    if Ta >= Ta_max:
        ventilation.on()
    elif RH >= RH_max:
        ventilation.on()
    else:
        ventilation.off()

    
def vent_Ta(Ta, Ta_max, GPIO=24):
    """
    Compares Ta with Ta_max. If statement is true/false ventilation starts/stops.
    
    Arguments:
        Ta (float): Actual air temperature measured with DHT22.
        Ta_max (int): Maximum air temperature accepted before ventialtion starts.
        GPIO (int): GPIO pin used to switch Relais for ventilation control.
    """

    ventilation = Relais.Relais(GPIO)
    if Ta >= Ta_max:
        ventilation.on()
    else:
        ventilation.off()


def vent_RH(RH, RH_max, GPIO=24):
    """
    Compares RH with RH_max. If statement is true/false ventilation starts/stops.
    
    Arguments:
        Ta (float): Actual air temperature measured with DHT22.
        RH (float): Actual humidity measured with DHT22.
        Ta_max (int): Maximum air temperature accepted before ventialtion starts.
        RH_max (int): Maximum humidity (in percent) accepted before ventilation starts.
        GPIO (int): GPIO pin used to switch Relais for ventilation control.
    """

    ventilation = Relais.Relais(GPIO)
    if RH >= RH_max:
        ventilation.on()
    else:
        ventilation.off()


if __name__ == '__main__':
    # Open JSON seetings file
    json_path = '/home/pi/Giess-o-mat/user_settings.json'
    ventilation_settings = read_json(json_path)

    # Write settinsg to variables
    if ventilation_settings['auto'] == True:
        if ventilation_settings['mode_ventilation_stop'] == True:
            # Get start and end time
            start_hour = int(ventilation_settings['start_time'][0:2])
            start_minute = int(ventilation_settings['start_time'][3:5])
            end_hour = int(ventilation_settings['end_time'][0:2])
            end_minute = int(ventilation_settings['end_time'][3:5])
            
            # Calculate start and end time in minutes
            start_time = start_hour*60 + start_minute
            end_time = end_hour*60 + end_minute

        elif ventilation_settings['mode_ventilation_stop'] == False:
            if ventilation_settings['mode'] == 'Lufttemperatursteuerung':
                # Get Ta from senor
                dht22 = DHT22.DHT22()
                Ta = dht22.get_temperature()
                # Get Ta threshold
                Ta_max = ventilation_settings['Ta_max']
                # Call function
                vent_Ta(Ta, Ta_max)
            elif ventilation_settings['mode'] == 'Luftfeuchtesteuerung':
                # Get RH from senor
                dht22 = DHT22.DHT22()
                RH = dht22.get_humidity()
                # Get RH threshold
                RH_max = ventilation_settings['RH_max']
                # Call function
                vent_RH(RH, RH_max)
            elif ventilation_settings['mode'] == 'Lufttemperatur- und Luftfeuchtesteuerung':
                # Get sensor values
                dht22 = DHT22.DHT22()
                Ta = dht22.get_temperature()
                RH = dht22.get_humidity()
                # Get thresholds
                Ta_max = ventilation_settings['Ta_max']
                RH_max = ventilation_settings['RH_max']
                # Call function
                vent_TaRH(Ta, RH, Ta_max, RH_max)