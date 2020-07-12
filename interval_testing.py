import time
from datetime import datetime, timedelta
from threading import Timer
from giessomat import Relais, RepeatedTimer

def calcdelta(daydelta, time):
    """
    Calculates the remaining time in seconds from the current time to a specified other point in time.

    Arguments:
        daydelta (int): Day interval.
        time (str): Next point in time to which the time difference will be calculated (form: 'hh:mm').
    """
    now = datetime.today()
    #nxt = now.replace(day=now.day, hour=int(time[0:2]), minute=int(time[3:5]), second=0, microsecond=0) + timedelta(days=daydelta)
    nxt = now.replace(day=now.day, hour=int(time[0:2]), minute=now.minute, second=0, microsecond=0) + timedelta(minutes=daydelta) #days=daydelta
    delta_t = nxt-now
    secs=delta_t.total_seconds()
    print('nxt: ', nxt)
    print('Delta (s): ', secs)
    return secs

def irrig_time(duration, GPIO=24):

    print("duration: ", duration)

    irrigation = Relais.Relais(GPIO)
    irrigation.on()
    time.sleep(duration)
    irrigation.off()

def test():
    print("Start: ", datetime.today())
    time.sleep(5)
    print("End: ", datetime.today())


def toggle_timer(t):
    if t.is_running:
        print('timer is alive, killing it')
        t.stop()
    else:
        t.start()
        print('timer is dead, starting it')

if __name__ == '__main__':
    #delta_secs = calcdelta(1, '12:40')
    
    for i in range(2):
        rt = RepeatedTimer.RepeatedTimer(30, test)
        #rt.start()
        toggle_timer(rt)

    #try:
    #    time.sleep(5) # your long-running job goes here...
    #finally:
    #    rt.stop()