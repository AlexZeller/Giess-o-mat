import datetime
from giessomat import Relais, DHT22, MCP3008, Photoresistor
# MCp3008 Ch:0 = Bodenfeuchte; Ch:1 = Fotowiederstand

# Get current temperature and humidity
dht22 = DHT22.DHT22(4)
Ta = dht22.get_temperature()
RH = dht22.get_humidity()

# Set sensor thresholds
soilH_min = 30 # soil humidity
Ta_max = 30 # maximum air temperature
RH_max = 80 # maximum air humidity
lux_threshold = 4000 # minimum lux value

# Set start and end time of lightning
start_hour = 7
start_minute = 0
end_hour = 21
end_minute = 00
# Calculate start and end time in minutes
start_time = int(start_hour)*60 + int(start_minute)
end_time = int(end_hour)*60 + int(end_minute)

############################################################################
def light_time(start, end):
    """
    Depending of the current time the light is switched on (start < current
    time < end )or off (start > current time, stop < current time).
    """

    # Light GPIO = 17
    light = Relais.Relais(17)
    current_time =  datetime.datetime.now().hour*60 + datetime.datetime.now().minute
    if start <= current_time and end >= current_time:
        light.on()
    else:
        light.off()


def light_time_light(start, end, lux_threshold):
    """
    Depending of the current time and the current lux_value the light is
    switched on (start < current time < end AND lux_value < lux threshold) or
    off (start > current time, stop < current time OR lux_value > lux_threshold).
    """

    light = Relais.Relais(17)
    photoresistor = Photoresistor.Photoresistor(1)
    # Get current lux value
    lux_reading = photoresistor.get_lux()
    
    current_time =  datetime.datetime.now().hour*60 + datetime.datetime.now().minute
    if lux_reading < lux_threshold and (start <= current_time and end >= current_time):
        light.on()
    else:
        light.off()

# To DO: Write the function! Not usable yet.
def ventilation_set(first, second, duration):
    """
    Ventilation is executed twice a day specified with first and second.
    """

    ventilation = Relais.Relais(18)


def ventilation_auto(Ta, RH, Ta_max, RH_max):
    """
    Compares Ta with Ta_max and RH with RH_max. If statement is true/false
    ventilation starts/stops.
    """

    # Ventilation GPIO = 18
    ventilation = Relais.Relais(18)
    if Ta >= Ta_max:
        ventilation.on()
    elif RH >= RH_max:
        ventilation.on()
    else:
        ventilation.off()


# To DO: Wie lange wird bewaessert?
def watering_auto(soilH, soilH_min):
    """
    Compares soilH with soilH_min. If statement is true watering starts.
    """

    # Pump GPIO = 
    pump = Relais.Relais()
    # Valve GPIO = 
    valve = Relais.Relais()
    if soilH <= soilH_min:
        valve.on()
        pump.on()
    else:
        pump.off()
        valve.off()


if __name__ == '__main__':
    #light_time(start_time, end_time)
    light_time_light(start_time, end_time, lux_threshold)
    ventilation_auto(Ta, RH, Ta_max, RH_max)
    
