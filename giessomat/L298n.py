import RPi.GPIO as GPIO          
import sys

class L298n:
    """ 
    Class to control two channels of a L298n Motor Module for fan speed control
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
        GPIO.setup(self.in1,GPIO.OUT)
        GPIO.setup(self.in2,GPIO.OUT)
        GPIO.setup(self.ena,GPIO.OUT) 
        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in2,GPIO.LOW)
        self.pwm=GPIO.PWM(self.ena,1000)
        self.pwm.start(0)
       

    def run(self, percentage):
        """ 
        Set the GPIO Pins to run the fans and control the speed. 
        
        Arguments: 
            percentage (int): The fan speed to bet set.
        """

        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in2,GPIO.HIGH)
        self.pwm.ChangeDutyCycle(percentage)

    def stop(self):
        """ 
        Stop the fans. (GPIO.cleanup())
        """

        GPIO.cleanup()

if __name__ == "__main__":

    try:
        in1_pin = 24
        in2_pin = 23
        ena_pin = 25
        status = sys.argv[1]
        try:
            percentage = int(sys.argv[2])
        except:
            pass

        l298 = L298n(in1_pin, in2_pin, ena_pin)
    
        if status == 'run':
            while True:
                l298.run(percentage)
        if status == 'stop':
            l298.stop()

    except KeyboardInterrupt:
        print('Stopped')