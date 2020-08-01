
import datetime
import time
import json
import sys
import psutil


with open('/home/pi/Giess-o-mat/giessomat/processes.json', 'r') as f:
    json_data = json.load(f)
    pid = json_data["fans"]
if psutil.pid_exists(pid):
    print(True)
else:
    print(False)
