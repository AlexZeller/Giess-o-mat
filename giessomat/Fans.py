import subprocess
import os
import signal
import sys
import json
import logging
import psutil

# Set up logging
log = logging.getLogger(__name__)

class Fans:
    """ 
    Class to control the speed of the 2 fans connected to the L298n motor module.
    Since the PWM is software controled a subprocess is spawned to keep the fans running.
    The id of the subprocess is written to a json file so it can be removed when the fans are stopped.

    Attributes: 
        json (string): The path of the proccesses.json file.   
        l298n (string): The path of the L298n module.   
    """

    def __init__(self, path_l298n, path_json):
        """ 
        The constructor for the Fans class.  

        Arguments: 
            path_l298b (string): The path of the L298n module. 
            path_json (string): The path of the subprocess.json file.
        """
        self.json = path_json
        self.l298n = path_l298n

    def start_fans(self, speed):
        """ 
        Start the Fans and set the speed. A subprocess gets spawned.

        Arguments: 
            speed (int): The speed of the fans in percent.
        """
        fan_subprocess = subprocess.Popen(
            ['python', self.l298n, 'run', str(speed)])
        log.debug('Opened L298n subprocess to run fans')
        fan_id = fan_subprocess.pid
        with open(self.json, 'r+') as f:
            json_data = json.load(f)
            json_data['fans'] = fan_id
            f.seek(0)
            f.write(json.dumps(json_data))
            f.truncate()
            log.debug('Wrote subprocess id to processes.json')

    def stop_fans(self):
        """ 
        Stop the fans. The subprocess gets killed.

        Arguments: 
            speed (int): The speed of the fans in percent.
        """
        with open(self.json, 'r') as f:
            json_data = json.load(f)
            pid = json_data["fans"]
        try:
            subprocess.Popen(['python', self.l298n, 'stop'])
            p = psutil.Process(pid)
            p.kill()
            #os.kill(pid, signal.SIGTERM)
            log.debug('Killed subprocess to stop fans')       
        except:
            raise
            log.debug('No such subprocess')
        

    def change_speed(self, speed):
        """ 
        Change the speed of the fans. A  new subprocess gets spawned.

        Arguments: 
            speed (int): The speed of the fans in percent.
        """
        fan_subprocess = subprocess.Popen(
            ['python', self.l298n, 'run', str(speed)])
        fan_id = fan_subprocess.pid
        with open(self.json, 'r+') as f:
            json_data = json.load(f)
            json_data['fans'] = fan_id
            f.seek(0)
            f.write(json.dumps(json_data))
            f.truncate()

    def get_status(self):
        """ 
        Check if fans are running.

        """
        with open(self.json, 'r') as f:
            json_data = json.load(f)
            pid = json_data["fans"]
        p = psutil.Process(pid=pid)
        if p.status() == psutil.STATUS_ZOMBIE:
            return False
        else:
            return True



if __name__ == "__main__":

    path_json = '/home/pi/Giess-o-mat/giessomat/processes.json'
    path_l298n = '/home/pi/Giess-o-mat/giessomat/L298n.py'

    try:
        status = sys.argv[1]
        try:
            speed = int(sys.argv[2])
        except:
            pass

        fans = Fans(path_l298n, path_json)
        if status == 'start':
            fans.start_fans(speed)
        if status == 'stop':
            fans.stop_fans()
        if status == 'change':
            fans.change_speed(speed)

    except:
        raise e
