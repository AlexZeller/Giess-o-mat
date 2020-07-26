import logging
from giessomat import LightControl
from giessomat import VentilationControl
from giessomat import IrrigationControl

# Set up logging
logging.basicConfig(filename='giessomat.log', filemode='w', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s', datefmt='%H:%M:%S')
log = logging.getLogger(__name__)

light_control = LightControl.LightControl(
    '/home/pi/Giess-o-mat-Webserver/light_settings.json')
ventilation_control = VentilationControl.VentilationControl(
    '/home/pi/Giess-o-mat-Webserver/ventilation_settings.json')
irrigation_control = IrrigationControl.IrrigationControl(
    '/home/pi/Giess-o-mat-Webserver/irrigation_settings.json')

# light_control.execute()
ventilation_control.execute()
# irrigation_control.execute()
