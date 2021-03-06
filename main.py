import datetime
from giessomat import Relais, DHT22, MCP3008, Photoresistor
# MCp3008 Ch:0 = Bodenfeuchte; Ch:2 = Fotowiederstand

# Get current temperature and humidity
dht22 = DHT22.DHT22(17)
Ta = dht22.get_temperature()
RH = dht22.get_humidity()

# Set sensor thresholds
soilH_min = 30 # soil humidity
Ta_max = 30 # maximum air temperature
RH_max = 70 # maximum air humidity
lux_threshold = 5000 # minimum lux value

# Set start and end time of lightning
start_hour = 6
start_minute = 0
end_hour = 22
end_minute = 00
# Calculate start and end time in minutes
start_time = int(start_hour)*60 + int(start_minute)
end_time = int(end_hour)*60 + int(end_minute)

############################################################################
def light_time(start, end, GPIO1=23, GPIO2=16):
    """
    Depending of the current time the light is switched on (start < current
    time < end )or off (start > current time, stop < current time).
    Arguments:
        start (int): Start time in minutes when lightning shall start.
        end (int): End time in minutes when lightning shall stop.
        GPIO (int): GPIO pin used to switch Relais for light control.
    """

    light1 = Relais.Relais(GPIO1)
    light2 = Relais.Relais(GPIO2)
    current_time =  datetime.datetime.now().hour*60 + datetime.datetime.now().minute
    if start <= current_time and end >= current_time:
        light1.on()
        light2.on()
    else:
        light1.off()
        light2.off()


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


def ventilation_set(times, GPIO=24):
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



def ventilation_auto(Ta, RH, Ta_max, RH_max, GPIO=24):
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


if __name__ == '__main__':
    light_time(start_time, end_time)
    #light_time_light(start_time, end_time, lux_threshold)
    ventilation_auto(Ta, RH, Ta_max, RH_max)
    #ventilation_set([[21, 45], [22,0]], GPIO=18)
    
