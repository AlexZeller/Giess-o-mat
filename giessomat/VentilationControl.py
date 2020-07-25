import datetime
import json
import sys
import logging
import Fans
import DHT22

# Set up logging
log = logging.getLogger(__name__)


class VentilationControl:

    def __init__(self, path_json):
        """
        Initializes the VentilationControl by reading the settings.json file.

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

    def execute(self):
        """
        Executes the main control function.
        """

        # Set up Fan control
        path_json = '/home/pi/Giess-o-mat/giessomat/processes.json'
        path_l298n = '/home/pi/Giess-o-mat/giessomat/L298n.py'
        fans = Fans.Fans(path_l298n, path_json)

        # Sensor values from DHT22 (air temperature and humidity)
        dht22 = DHT22.DHT22(17)
        Ta = dht22.get_temperature()
        Rh = dht22.get_humidity()

        # get setting info
        start_time = self.settings['start_time']
        end_time = self.settings['end_time']
        Ta_threshold = int(self.settings['Ta_max'])
        Rh_threshold = int(self.settings['Rh_max'])
        mode = self.settings['mode']
        night_mode = self.settings['mode_ventilation_stop']

        if mode == 'Manuell':
            log.info('Mode: Manuell')
            return
        if night_mode and self.check_if_time_inbetween(start_time, end_time):
            log.info('Nachtruhe. Fans off.')
            fans.stop_fans()
        else:
            if mode == 'Lufttemperatursteuerung':
                log.info('Mode: Lufttemperatursteuerung')
                if Ta > Ta_threshold:
                    log.info('Ta > Threshold. Turning Fans on')
                    fans.start_fans(25)
                else:
                    log.info('Ta < Threshold. Fans off')
                    fans.stop_fans()

            elif mode == 'Luftfeuchtesteuerung':
                log.info('Mode: Luftfeuchtesteuerung')
                if Rh > Rh_threshold:
                    log.info('Rh > Threshold. Turning Fans on')
                    fans.start_fans(25)
                else:
                    log.info('Rh < Threshold. Fans off')
                    fans.stop_fans()

            elif mode == 'Lufttemperatur- und Luftfeuchtesteuerung':
                log.info('Mode: Lufttemperatur- und Luftfeuchtesteuerung')
                if Rh > Rh_threshold or Ta > Ta_threshold:
                    log.info('Rh or Ta > Threshold. Turning Fans on')
                    fans.start_fans(25)
                else:
                    log.info('Rh or Ta < Threshold. Fans off')
                    fans.stop_fans()

            else:
                log.error('Mode not recognised')


if __name__ == "__main__":
    try:
        ventilationcontrol = VentilationControl(
            '/home/pi/Giess-o-mat-Webserver/ventilation_settings.json')
        ventilationcontrol.execute()
    except:
        raise
