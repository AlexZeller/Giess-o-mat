import datetime
import logging
import time
import json
import sys
import Relais
import SoilMoisture
import Database

# Set up logging
log = logging.getLogger(__name__)
db = Database.Database('/home/pi/Giess-o-mat/giessomat_db.db')


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

        return delta_days % interval == 0

    def check_if_time(self, time):
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

    def execute(self, GPIO=23, channel=0):
        """
        Executes the main control function.

        Arguments:
            GPIO (int): The GPIO of the Relais Channel
            channel (int): The channel of the photoresistor
        """

        # Set up Relais and soil moisture reading
        soilmoisture = SoilMoisture.SoilMoisture(channel)
        moisture_reading = soilmoisture.get_volumetric_water_content()
        irrigation = Relais.Relais(GPIO)

        # get setting info
        mode = self.settings['mode']
        interval = int(self.settings['interval'])
        number_irrigations = int(self.settings['number_irrigations'])
        duration_irrigation = int(self.settings['duration_irrigation'])
        irrigation_time_1 = self.settings['irrigation_time_1']
        irrigation_time_2 = self.settings['irrigation_time_2']
        irrigation_time_3 = self.settings['irrigation_time_3']
        moisture_threshold = int(self.settings['humidity_threshold'])
        mode = self.settings['mode']
        timestamp = self.settings['timestamp']

        if mode == 'Manuell':
            log.info('Mode: Manuell')
            return
        elif mode == 'Zeitsteuerung':
            log.info('Mode: Zeitsteuerung')
            # check if it is an irrigation day
            if self.check_if_day(interval, timestamp):
                log.debug('Interval returns irrigation day')
                # only if interval = 1 multiple irrigation times are possible
                if interval == 1:
                    if number_irrigations == 1:
                        log.debug('Number of irrigations = 1')
                        if self.check_if_time(irrigation_time_1):
                            log.info(
                                'Current time IS irrigation time (buffer)')
                            log.info('Turning irrigation ON')
                            db.log2database('Irrigation', 'action', 'Irrigation based on "Zeitsteuerung"')
                            irrigation.on()
                            time.sleep(duration_irrigation)
                            log.info('Turning irrigation OFF')
                            irrigation.off()
                        else:
                            log.info('Current time is NOT irrigation time')

                    if number_irrigations == 2:
                        log.debug('Number of irrigations = 2')
                        if self.check_if_time(irrigation_time_1):
                            log.info(
                                'Current time IS irrigation time (buffer)')
                            log.info('Turning irrigation ON')
                            db.log2database('Irrigation', 'action', 'Irrigation based on "Zeitsteuerung"')
                            irrigation.on()
                            time.sleep(duration_irrigation)
                            log.info('Turning irrigation OFF')
                            irrigation.off()
                        if self.check_if_time(irrigation_time_2):
                            log.info(
                                'Current time IS irrigation time (buffer)')
                            log.info('Turning irrigation ON')
                            db.log2database('Irrigation', 'action', 'Irrigation based on "Zeitsteuerung"')
                            irrigation.on()
                            time.sleep(duration_irrigation)
                            log.info('Turning irrigation OFF')
                            irrigation.off()
                        else:
                            log.info('Current time is NOT irrigation time')

                    if number_irrigations == 3:
                        log.debug('Number of irrigations = 3')
                        if self.check_if_time(irrigation_time_1):
                            log.info(
                                'Current time IS irrigation time (buffer)')
                            log.info('Turning irrigation ON')
                            db.log2database('Irrigation', 'action', 'Irrigation based on "Zeitsteuerung"')
                            irrigation.on()
                            time.sleep(duration_irrigation)
                            log.info('Turning irrigation OFF')
                            irrigation.off()
                        if self.check_if_time(irrigation_time_2):
                            log.info(
                                'Current time IS irrigation time (buffer)')
                            log.info('Turning irrigation ON')
                            db.log2database('Irrigation', 'action', 'Irrigation based on "Zeitsteuerung"')
                            irrigation.on()
                            time.sleep(duration_irrigation)
                            log.info('Turning irrigation OFF')
                            irrigation.off()
                        if self.check_if_time(irrigation_time_3):
                            log.info(
                                'Current time IS irrigation time (buffer)')
                            log.info('Turning irrigation ON')
                            db.log2database('Irrigation', 'action', 'Irrigation based on "Zeitsteuerung"')
                            irrigation.on()
                            time.sleep(duration_irrigation)
                            log.info('Turning irrigation OFF')
                            irrigation.off()
                        else:
                            log.info('Current time is NOT irrigation time')
                # all other intervals only have 1 irrigation time
                else:
                    if self.check_if_time(irrigation_time_1):
                        log.info('Current time IS irrigation time (buffer)')
                        log.info('Turning irrigation ON')
                        db.log2database('Irrigation', 'action', 'Irrigation based on "Zeitsteuerung"')
                        irrigation.on()
                        time.sleep(duration_irrigation)
                        log.info('Turning irrigation OFF')
                        irrigation.off()

                    else:
                        log.info('Current time is NOT irrigation time')
                        return
            else:
                log.info('Interval returns NO irrigation day')
                return

        elif mode == 'Bodenfeuchtesteuerung':
            log.info('Mode: Bodenfeuchtesteuerung')
            # To be done

        elif mode == 'Zeit- und Bodenfeuchtesteuerung':
            log.info('Mode: Zeit- und Bodenfeuchtesteuerung')
            # check if it is an irrigation day
            if self.check_if_day(interval, timestamp):
                log.debug('Interval returns irrigation day')
                # only if interval = 1 multiple irrigation times are possible
                if interval == 1:
                    if number_irrigations == 1:
                        log.debug('Number of irrigations = 1')
                        if self.check_if_time(irrigation_time_1):
                            log.info(
                                'Current time IS irrigation time (buffer)')
                            if moisture_reading < moisture_threshold:
                                log.info(
                                    'Moisture reading below moisture threshold')
                                log.info('Turning irrigation ON')
                                db.log2database('Irrigation', 'action', 'Irrigation based on "Zeit- und Bodenfeuchtesteuerung"')
                                irrigation.on()
                                time.sleep(duration_irrigation)
                                log.info('Turning irrigation OFF')
                                irrigation.off()
                            else:
                                log.info(
                                    'Moisture reading above moisture threshold. NO irrigation')
                                return
                        else:
                            log.info('Current time is NOT irrigation time')

                    if number_irrigations == 2:
                        log.debug('Number of irrigations = 2')
                        if self.check_if_time(irrigation_time_1):
                            log.info(
                                'Current time IS irrigation time (buffer)')
                            if moisture_reading < moisture_threshold:
                                log.info(
                                    'Moisture reading below moisture threshold')
                                log.info('Turning irrigation ON')
                                db.log2database('Irrigation', 'action', 'Irrigation based on "Zeit- und Bodenfeuchtesteuerung"')
                                irrigation.on()
                                time.sleep(duration_irrigation)
                                log.info('Turning irrigation OFF')
                                irrigation.off()
                            else:
                                log.info(
                                    'Moisture reading above moisture threshold. NO irrigation')
                                return
                        if self.check_if_time(irrigation_time_2):
                            log.info(
                                'Current time IS irrigation time (buffer)')
                            if moisture_reading < moisture_threshold:
                                log.info(
                                    'Moisture reading below moisture threshold')
                                log.info('Turning irrigation ON')
                                db.log2database('Irrigation', 'action', 'Irrigation based on "Zeit- und Bodenfeuchtesteuerung"')
                                irrigation.on()
                                time.sleep(duration_irrigation)
                                log.info('Turning irrigation OFF')
                                irrigation.off()
                            else:
                                log.info(
                                    'Moisture reading above moisture threshold. NO irrigation')
                                return
                        else:
                            log.info('Current time is NOT irrigation time')

                    if number_irrigations == 3:
                        log.debug('Number of irrigations = 3')
                        if self.check_if_time(irrigation_time_1):
                            log.info(
                                'Current time IS irrigation time (buffer)')
                            if moisture_reading < moisture_threshold:
                                log.info(
                                    'Moisture reading below moisture threshold')
                                log.info('Turning irrigation ON')
                                db.log2database('Irrigation', 'action', 'Irrigation based on "Zeit- und Bodenfeuchtesteuerung"')
                                irrigation.on()
                                time.sleep(duration_irrigation)
                                log.info('Turning irrigation OFF')
                                irrigation.off()
                            else:
                                log.info(
                                    'Moisture reading above moisture threshold. NO irrigation')
                                return
                        if self.check_if_time(irrigation_time_2):
                            log.info(
                                'Current time IS irrigation time (buffer)')
                            if moisture_reading < moisture_threshold:
                                log.info(
                                    'Moisture reading below moisture threshold')
                                log.info('Turning irrigation ON')
                                db.log2database('Irrigation', 'action', 'Irrigation based on "Zeit- und Bodenfeuchtesteuerung"')
                                irrigation.on()
                                time.sleep(duration_irrigation)
                                log.info('Turning irrigation OFF')
                                irrigation.off()
                            else:
                                log.info(
                                    'Moisture reading above moisture threshold. NO irrigation')
                                return
                        if self.check_if_time(irrigation_time_3):
                            log.info(
                                'Current time IS irrigation time (buffer)')
                            if moisture_reading < moisture_threshold:
                                log.info(
                                    'Moisture reading below moisture threshold')
                                log.info('Turning irrigation ON')
                                db.log2database('Irrigation', 'action', 'Irrigation based on "Zeit- und Bodenfeuchtesteuerung"')
                                irrigation.on()
                                time.sleep(duration_irrigation)
                                log.info('Turning irrigation OFF')
                                irrigation.off()
                            else:
                                log.info(
                                    'Moisture reading above moisture threshold. NO irrigation')
                                return
                        else:
                            log.info('Current time is NOT irrigation time')
                # all other intervals only have 1 irrigation time
                else:
                    if self.check_if_time(irrigation_time_1):
                        log.info('Current time IS irrigation time (buffer)')
                        if moisture_reading < moisture_threshold:
                            log.info(
                                'Moisture reading below moisture threshold')
                            log.info('Turning irrigation ON')
                            db.log2database('Irrigation', 'action', 'Irrigation based on "Zeit- und Bodenfeuchtesteuerung"')
                            irrigation.on()
                            time.sleep(duration_irrigation)
                            log.info('Turning irrigation OFF')
                            irrigation.off()
                        else:
                            log.info(
                                'Moisture reading above moisture threshold. NO irrigation')
                            return

                    else:
                        log.info('Current time is NOT irrigation time')
                        return
            else:
                log.info('Interval returns NO irrigation day')
                return

        else:
            log.exception('Mode not recognised')


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    try:
        irrigationcontrol = IrrigationControl(
            '/home/pi/Giess-o-mat-Webserver/irrigation_settings.json')
        irrigationcontrol.execute()
    except:
        raise
