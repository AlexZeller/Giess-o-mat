import eventlet
import socketio
from Fans import Fans

path_json = '/home/pi/Giess-o-mat/giessomat/processes.json'
path_l298n = '/home/pi/Giess-o-mat/giessomat/L298n.py'

fans = Fans.Fans(path_l298n, path_json)


sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)


@sio.event
def connect(sid, environ):
    print('connect', sid)
    sio.emit('message', 'Test')


@sio.event
def fan(sid, data):
    if data == True:
        fans.start_fans(50)
        print('started fans')
    if data == False:
        fans.stop_fans()


@sio.event
def disconnect(sid):
    print('disconnect', sid)


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
