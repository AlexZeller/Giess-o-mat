
import datetime
import time
import json
import sys
import psutil


with open('/home/pi/Giess-o-mat/giessomat/processes.json', 'r') as f:
    json_data = json.load(f)
    pid = json_data["fans"]
    print pid
    p = psutil.Process(pid=pid)
    print(p.status())
    if p.status() == psutil.STATUS_ZOMBIE:
        print(False)
    else:
        print(True)
  

    
