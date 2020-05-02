#!/usr/bin/env python2
###############################################################################
import datetime

from giessomat import Relais, DHT22, MCP3008
# MCp3008 Ch:0 = Bodenfeuchte; Ch:1 = Fotowiederstand
# Get current temperature and humidity
dht22 = DHT22.DHT22(4)
Ta = dht22.get_temperature()
RH = dht22.get_humidity()
# Set thresholds
# soil humidity
soilH_min = 30
# maximum air temperature
Ta_max = 30
# maximum air humidity
RH_max = 80

# Set start and end time of lightning
start_hour = 7
start_minute = 0
end_hour = 21
end_minute = 00
# Calculate start and end time in minutes
start_time = int(start_hour)*60 + int(start_minute)
end_time = int(end_hour)*60 + int(end_minute)

###############################################################################
def light_auto(start, end):
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
    light_auto(start_time, end_time)
    ventilation_auto(Ta, RH, Ta_max, RH_max)
    
