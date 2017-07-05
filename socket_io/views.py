from django.shortcuts import render
import socketio
from users.backends import JWTAuthentication

sio = socketio.Server(async_mode='gevent')


@sio.on('connect')
def test_connect(sid, environ):
    try:
        auth = JWTAuthentication()
        data = auth.socket_authenticate(environ['HTTP_AUTHORIZATION'])
        print('connected sa')
        print(data[0])
        if data and data[0]:
            environ['user'] = data[0]
        else:
            return False
    except Exception as err:
        print(err)
        return False



@sio.on('test_event')
def test_event(sid, message):
    print('message from socket:')
   # print(sio.environ[sid]['HTTP_AUTHORIZATION'])
    print(sio.environ[sid]['user'])
    print(sio.environ[sid]['user'].id)
    print(sid)

    # to all
    #sio.emit('django',{'kkk':'sss'})

    #to one
    #sio.emit('django',{'kkk':'sss1'}, room=sid)

    #without me
    #sio.emit('django',{'kinder':'lol'},skip_sid=sid)


def index(request):
    return render(request, 'index.html', {})

# Create your views here.
