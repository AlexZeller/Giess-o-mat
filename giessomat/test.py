
import datetime
import time
import json
import sys


with open('/home/pi/Giess-o-mat-Webserver/irrigation_settings.json') as f:
    settings = json.load(f)


irrigation_settings = settings

#current_time = datetime.datetime.now().strftime("%H:%M")

def get_delta_days(timestamp_settings):
    """
    Takes a utc timestamp and returns the number of days between
    the timestamp and the current date.

    Arguments:
        timestamp_settings (int): UTC timestamp.
    """

    timestamp_now = time.time()
    datetime_settings = datetime.datetime.fromtimestamp(timestamp_settings)
    print(datetime_settings)
    datettime_now = datetime.datetime.fromtimestamp(timestamp_now)
    print(datettime_now)
    delta_time = datettime_now.date()-datetime_settings.date()

    return(delta_time.days)

def check_if_time(time):
    """
    Takes a times (HH:MM) and returns True if the current time
    is within an additional 5 minutes of the give time, otherwise False.

    Arguments:
        start_time (str): start time.
        end_time (str): end time.
    """

    # get current time
    current_time = datetime.datetime.now().strftime("%H:%M")
    time_buffer_datetime = datetime.datetime.strptime(
        time, "%H:%M") + datetime.timedelta(seconds=300)
    time_buffer = time_buffer_datetime.strftime("%H:%M")

    log.debug('Current time: ' + current_time)
    log.debug('Irrigation time: ' + time)

    # check if current time in between start and end time
    if time < time_buffer:
        return current_time >= time and current_time < time_buffer
    else:
        # in case times cross midnight
        return time >= current_time or current_time < time_buffer



test = check_if_time(irrigation_settings['timestamp'])
print(test)
