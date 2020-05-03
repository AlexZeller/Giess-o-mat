import subprocess
import os
import signal
import sys
import json


class Fans:
    def __init__(self):
        self.json = '/home/pi/Giess-o-mat/giessomat/processes.json'

    def start_fans(self, speed):
        fan_subprocess = subprocess.Popen(['python', '/home/pi/Giess-o-mat/giessomat/L298n.py', 'run', str(speed)])
        fan_id = fan_subprocess.pid
        with open(self.json, 'r+') as f:
            json_data = json.load(f)
            json_data['fans'] = fan_id
            f.seek(0)
            f.write(json.dumps(json_data))
            f.truncate()

    def stop_fans(self):
        with open(self.json, 'r') as f:
            json_data = json.load(f)
            pid = json_data["fans"] 
        os.kill(pid, signal.SIGTERM)
        subprocess.call(['python', '/home/pi/Giess-o-mat/giessomat/L298n.py', 'stop'])

    def change_speed(self, speed):
        fan_subprocess = subprocess.Popen(['python', '/home/pi/Giess-o-mat/giessomat/L298n.py', 'run', str(speed)])
        
if __name__ == "__main__":

    try:
        status = sys.argv[1]
        try:
            speed = int(sys.argv[2])
        except:
            pass
        print('Controlling Fans...')
    
        fans = Fans()
        if status == 'start':
            fans.start_fans(speed)
        if status == 'stop':
            fans.stop_fans()
        if status == 'change':
            fans.stop_fans(speed)

    except KeyboardInterrupt:
        print('Stopped')
