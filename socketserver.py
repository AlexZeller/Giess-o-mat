from giessomat import Relais
from giessomat import Fans
import eventlet
import socketio

eventlet.monkey_patch()


path_json = '/home/pi/Giess-o-mat/giessomat/processes.json'
path_l298n = '/home/pi/Giess-o-mat/giessomat/L298n.py'

relais_light = Relais.Relais(24)
relais_irrigation = Relais.Relais(23)


fans = Fans.Fans(path_l298n, path_json)

mgr = socketio.KombuManager('amqp://')
sio = socketio.Server(cors_allowed_origins=[
                      'http://localhost:5672', 'http://192.168.0.134:8080', 'http://192.168.0.235'], client_manager=mgr)

#sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)


@sio.event
def connect(sid, environ):
    print('connect', sid)


@sio.event
def fan(sid, data):
    if data == True:
        fans.start_fans(10)
        print('started fans')
    if data == False:
        fans.stop_fans()


@sio.event
def light(sid, data):
    if data == True:
        print(data)
        relais_light.on()
    if data == False:
        print(data)
        relais_light.off()


@sio.event
def irrigationn(sid, data):
    if data == True:
        print(data)
        relais_irrigation.on()
    if data == False:
        print(data)
        relais_irrigation.off()


@sio.event
def disconnect(sid):
    print('disconnect', sid)


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
