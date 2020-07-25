import datetime
import time
import json
import sys
import Relais
import SoilMoisture

# Set up logging
log = logging.getLogger(__name__)


class IrrigationControl:

    def __init__(self, path_json):
        """
        Initializes the IrrigationControl by reading the settings.json file.

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

    def get_delta_days(self, timestamp_settings):
        """
        Takes a utc timestamp and returns the number of days between
        the timestamp and the current date.

        Arguments:
            timestamp_settings (int): UTC timestamp.
        """

        timestamp_now = time.time()
        datetime_settings = datetime.datetime.fromtimestamp(timestamp_settings)
        datettime_now = datetime.datetime.fromtimestamp(timestamp_now)
        delta_time = datettime_now.date()-datetime_settings.date()

        return(delta_time.days)

    def check_if_day(self, interval, timestamp_settings):
        """
        Takes an interval (int) and a timestamp and returns True if the current date
        has a distance to the timestamp of a multiple of the interval, otherwise False.

        Arguments:
            interval (int): Interval.
        """
        delta_days = self.get_delta_days(timestamp_settings)

        return delta_days % interval == 0:

    def check_if_time(self, time):
        """
        Takes a times (HH:MM) and returns True if the current time
        is within an additional two minutes of the give time, otherwise False.

        Arguments:
            start_time (str): start time.
            end_time (str): end time.
        """

        # get current time
        current_time = datetime.datetime.now().strftime("%H:%M")
        time_buffer_datetime = datetime.datetime.now() + datetime.timedelta(seconds=120)
        time_buffer = time_buffer_datetime..strftime("%H:%M")

        # check if current time in between start and end time
        if time < time_buffer:
            return current_time > time and current_time < time_buffer
        else:
            # in case times cross midnight
            return current_time > time or current_time < time_buffer

    def execute(self, GPIO=24, channel=2):
        """
        Executes the main control function.

        Arguments:
            GPIO (int): The GPIO of the Relais Channel
            channel (int): The channel of the photoresistor
        """

        # get setting info
        mode = self.settings['mode']
        interval = int(self.settings['interval'])
        number_irrigations = int(self.settings['number_irrigations'])
        duration_irrigation = int(self.settings['duration_irrigation'])
        irrigation_time_1 = self.settings['irrigation_time_1']
        irrigation_time_2 = self.settings['irrigation_time_2']
        irrigation_time_3 = self.settings['irrigation_time_3']
        humidity_threshold = int(self.settings['humidity_threshold'])
        mode = self.settings['mode']

        if mode == 'Manuell':
            log.info('Mode: Manuell')
            return
        elif mode == 'Zeitsteuerung':
            log.info('Mode: Zeitsteuerung')

        elif mode == 'Bodenfeuchtesteuerung':
            log.info('Mode: Bodenfeuchtesteuerung')

        elif mode == 'Zeit- und Bodenfeuchtesteuerung':
            log.info('Mode: Zeit- und Bodenfeuchtesteuerung')

        else:
            log.error('Mode not recognised')


if __name__ == "__main__":
    try:
        irrigationcontrol = IrrigationControl(
            '/home/pi/Giess-o-mat-Webserver/irrigation_settings.json')
        irrigationcontrol.execute()
    except:
        raise
