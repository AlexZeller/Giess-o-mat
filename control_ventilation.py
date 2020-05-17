import datetime
from giessomat import Relais, DHT22

# Ventilation mode_sensor:
    # Values  
        # "Ta" >  Ta controlled 
        # "RH" > RH controlled
        # "TaRH" > Ta and RH controlled
# Ventilation mode_times:
    # Values
        # "true" > always set at specific times
        # "false" > Not considered
# Ventilation mode_time_window (not yet implemented):
    # Values
        # "true" > just within time window
        # "false" > Not considered

# Set start and end time of ventilation
start_hour = 6
start_minute = 0
end_hour = 22
end_minute = 00

# Calculate start and end time in minutes
start_time = int(start_hour)*60 + int(start_minute)
end_time = int(end_hour)*60 + int(end_minute)

# Set sensor thresholds
soilH_min = 30 # soil humidity
Ta_max = 30 # maximum air temperature
RH_max = 70 # maximum air humidity
lux_threshold = 5000 # minimum lux value

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
    ventilation_settings = read_json(json_path, 'ventilation')

    # Write settinsg to variables
    if ventilation_settings['auto'] == False:
        if ventilation_settings['mode_sensor'] == 'Ta':
            # Get Ta from senor
            dht22 = DHT22.DHT22()
            Ta = dht22.get_temperature()
            # Get Ta threshold
            Ta_max = ventilation_settings['Ta_max']
            # Call function
            vent_Ta(Ta, Ta_max)
        elif ventilation_settings['mode_sensor'] == 'RH':
            # Get RH from senor
            dht22 = DHT22.DHT22()
            RH = dht22.get_humidity()
            # Get RH threshold
            RH_max = ventilation_settings['RH_max']
            # Call function
            vent_RH(RH, RH_max)
        elif ventilation_settings['mode_sensor'] == 'TaRH':
            # Get sensor values
            dht22 = DHT22.DHT22()
            Ta = dht22.get_temperature()
            RH = dht22.get_humidity()
            # Get thresholds
            Ta_max = ventilation_settings['Ta_max']
            RH_max = ventilation_settings['RH_max']
            # Call function
            vent_TaRH(Ta, RH, Ta_max, RH_max)
        elif 



        start_hour = ventilation_settings['start_hour']
        start_minute = ventilation_settings['start_min']
        end_hour = ventilation_settings['end_hour']
        end_minute = ventilation_settings['end_min']
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