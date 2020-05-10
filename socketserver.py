import eventlet
import socketio
from giessomat import Relais

#path_json = '/home/pi/Giess-o-mat/giessomat/processes.json'
#path_l298n = '/home/pi/Giess-o-mat/giessomat/L298n.py'

relais_light = Relais.Relais(17)
relais_fan = Relais.Relais(18)


#fans = Fans.Fans(path_l298n, path_json)


sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)


@sio.event
def connect(sid, environ):
    print('connect', sid)
    sio.emit('message', 'Test')


#@sio.event
#def fan(sid, data):
#    if data == True:
#        fans.start_fans(50)
#       print('started fans')
#    if data == False:
#        fans.stop_fans()

@sio.event
def light(sid, data):
    if data == True:
        print(data)
        relais_light.on()
    if data == False:
        print(data)
        relais_light.off()

@sio.event
def fan(sid, data):
    if data == True:
        print(data)
        relais_fan.on()
    if data == False:
        print(data)
        relais_fan.off()


@sio.event
def disconnect(sid):
    print('disconnect', sid)


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
