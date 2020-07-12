from threading import Timer

class RepeatedTimer(object):
    """
    Class to execute a function always in a specific interval.

    Attributes:
        interval (int): Interval in seconds when function is executed.
        function (callable): Function which will be executed in a so+pecific interval.
        args
    """
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        #self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False


if __name__ == '__main__':
    def test_function():
        print("Function is executed")

    rt = RepeatedTimer(60, test_function)
    if not rt.is_running:
        rt.start()