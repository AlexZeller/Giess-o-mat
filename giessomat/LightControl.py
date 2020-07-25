import datetime
import json
import sys
import Relais
import Photoresistor


class LightControl:

    def __init__(self, path_json):
        """
        Initializes the LightControl by reading the settings.json file.

        Arguments:
            path_json (str): Path to json file.
        """

        with open(path_json) as f:
            settings = json.load(f)

        self.settings = settings

    def check_if_time_inbetween(self, start_time, end_time):
        """
        Takes two times (HH:MM) and returns True if the current time
        is in between the two times, otherwise False.

        Arguments:
            start_time (str): start time.
            end_time (str): end time.
        """

        # get current time
        current_time = datetime.datetime.now().strftime("%H:%M")

        if start_time < end_time:
            return current_time > start_time and current_time < end_time
        else:
            # in case times cross midnight
            return current_time > start_time or current_time < end_time

    def execute(self, GPIO=24, channel=2):

        light = Relais.Relais(GPIO)
        photoresistor = Photoresistor.Photoresistor(channel)
        lux_reading = photoresistor.get_lux()

        start_time = self.settings['start_time']
        end_time = self.settings['end_time']

        mode = self.settings['mode']

        if mode == 'Manuell':
            return
        elif mode == 'Zeitsteuerung':
            if self.check_if_time_inbetween(start_time, end_time) == True:
                light.on()
            else:
                light.off()
        elif mode == 'Zeit- und Helligkeitssteuerung' == True:
            lux_threshold = self.settings['lux_threshold']
            if self.check_if_time_inbetween(start_time, end_time) and lux_reading < lux_threshold:
                light.on()
            else:
                light.off()
        else:
            print('mode not recognised')


if __name__ == "__main__":
    try:
        lightcontrol = LightControl(
            '/home/pi/Giess-o-mat-Webserver/light_settings.json')
        lightcontrol.execute()
    except:
        raise
