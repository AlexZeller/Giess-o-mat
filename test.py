########### This is a temporary test file. Can be overwritten at any point #########
import socketio
from giessomat import Fans

path_json = '/home/pi/Giess-o-mat/giessomat/processes.json'
path_l298n = '/home/pi/Giess-o-mat/giessomat/L298n.py'

mgr = socketio.KombuManager('amqp://')
sio = socketio.Server(client_manager=mgr)

fans = Fans.Fans(path_l298n, path_json)

fans.stop_fans()
sio.emit('fan', False)
