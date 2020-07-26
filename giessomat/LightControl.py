import datetime
import logging
import json
import sys
import Relais
import Photoresistor

# Set up logging
log = logging.getLogger(__name__)


class LightControl:

    def __init__(self, path_json):
        """
        Initializes the LightControl by reading the settings.json file.

        Arguments:
            path_json (str): Path to json file.
        """
        try:
            with open(path_json) as f:
                settings = json.load(f)
                log.debug('Loaded .json settings')
        except:
            log.exception()

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

        # check if current time in between start and end time
        if start_time < end_time:
            return current_time > start_time and current_time < end_time
        else:
            # in case times cross midnight
            return current_time > start_time or current_time < end_time

    def execute(self, GPIO=24, channel=2):
        """
        Executes the main control function.

        Arguments: 
            GPIO (int): The GPIO of the Relais Channel
            channel (int): The channel of the photoresistor
        """

        # Set up Relais and Photoresistor reading
        light = Relais.Relais(GPIO)
        photoresistor = Photoresistor.Photoresistor(channel)
        lux_reading = photoresistor.get_lux()

        # get setting info
        start_time = self.settings['start_time']
        end_time = self.settings['end_time']
        mode = self.settings['mode']
        lux_threshold = int(self.settings['lux_threshold'])

        if mode == 'Manuell':
            log.info('Mode: Manuell')
            return
        elif mode == 'Zeitsteuerung':
            log.info('Mode: Zeitsteuerung')
            if self.check_if_time_inbetween(start_time, end_time):
                log.info('In between set time. Light on.')
                light.on()
            else:
                log.info('Not in between set time. Light off.')
                light.off()
        elif mode == 'Zeit- und Helligkeitssteuerung':
            log.info('Mode: Zeit- und Helligkeitssteuerung')
            if self.check_if_time_inbetween(start_time, end_time) and lux_reading < lux_threshold:
                log.info('Lux reading under threshold. Light on.')
                light.on()
            else:
                log.info('Lux reading above threshold. Light off.')
                light.off()
        else:
            log.error('Mode not recognised')


if __name__ == "__main__":
    try:
        lightcontrol = LightControl(
            '/home/pi/Giess-o-mat-Webserver/light_settings.json')
        lightcontrol.execute()
    except:
        raise
