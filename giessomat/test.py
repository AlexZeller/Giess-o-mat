
import datetime
import json
import sys


with open('/home/pi/Giess-o-mat-Webserver/light_settings.json') as f:
    settings = json.load(f)


light_settings = settings

#current_time = datetime.datetime.now().strftime("%H:%M")


start_time = light_settings['start_time']
end_time = light_settings['end_time']


def check_if_time_inbetween(start_time, end_time):
    """
    Takes two times (HH:MM) and returns True if the current time
    is in between the two times, otherwise False.

    Arguments:
        start_time (str): start time.
        end_time (str): end time.
    """

    # get current time
    current_time = datetime.datetime.now().strftime("%H:%M")
    print(current_time)

    if start_time < end_time:
        return current_time > start_time and current_time < end_time
    else:
        # in case times cross midnight
        return current_time > start_time or current_time < end_time


test = check_if_time_inbetween(start_time, end_time)
print(test)
