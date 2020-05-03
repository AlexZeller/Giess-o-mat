########### This is a temporary test file. Can be overwritten at any point #########
from time import sleep
import subprocess
import os
import signal

fan = subprocess.Popen(['python', '/home/pi/Giess-o-mat/giessomat/L298n.py', 'run', '10'])
fan_id = fan.pid
print fan_id
sleep(10)


subprocess.call(['python', '/home/pi/Giess-o-mat/giessomat/L298n.py', 'stop'])
os.kill(fan_id, signal.SIGTERM)