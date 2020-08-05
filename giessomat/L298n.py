import RPi.GPIO as GPIO
import sys
import time


class L298n:
    """ 
    Class to control two channels of a L298n Motor Module 
    Attributes: 
        in1 (int): The number of IN1 Pin. 
        in2 (int): The number of IN2 Pin.   
        ena (int): The number of ENA Pin.
        pwm (int): The PWM object.     
    """

    def __init__(self, in1_pin, in2_pin, ena_pin):
        """ 
        The constructor for the L298n class. 

        Arguments: 
            in1 (int): The number of IN1 Pin. 
            in2 (int): The number of IN2 Pin.   
            ena (int): The number of ENA Pin. 
        """

        self.in1 = in1_pin
        self.in2 = in2_pin
        self.ena = ena_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.in1, GPIO.OUT)
        GPIO.setup(self.in2, GPIO.OUT)
        GPIO.setup(self.ena, GPIO.OUT)
        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.LOW)
        self.pwm = GPIO.PWM(self.ena, 20500)

    def run(self, percentage):
        """ 
        Set the GPIO Pins to run the dc motor and control the speed. 

        Arguments: 
            percentage (int): The pwm duty cycle in percent.
        """
        while True:
            GPIO.output(self.in1, GPIO.HIGH)
            GPIO.output(self.in2, GPIO.LOW)
            self.pwm.start(percentage)
            time.sleep(1)

    def stop(self):
        """ 
        Stop the motor. (GPIO.cleanup())
        """

        GPIO.cleanup()


if __name__ == "__main__":

    # This main function will be called as a subprocess by the Fans module
    # The pins have to be set accordingly

    try:
        in1_pin = 21
        in2_pin = 26
        ena_pin = 20
        status = sys.argv[1]
        try:
            percentage = int(sys.argv[2])
        except:
            pass

        l298 = L298n(in1_pin, in2_pin, ena_pin)

        if status == 'run':
            l298.run(percentage)
        if status == 'stop':
            l298.stop()

    except KeyboardInterrupt:
        print('Stopped')
        GPIO.cleanup()
