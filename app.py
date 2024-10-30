
from flask import Flask,request
from flask_socketio import SocketIO , emit,join_room

app = Flask(__name__)
app.secret_key = 'This is a secret key'

socketio = SocketIO(app,cors_allowed_origins="*")


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello People!'

@socketio.on('join')
def join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    print(f"{username} has joined the room {room}")
    emit('ready',{username:username},to=room,skip_sid=request.sid)

@socketio.on('data')
def send_data(data):
    username = data['username']
    room = data['room']
    message = data['data']
    print(f"{username} has sent {message} in room{room}")
    emit('data',data,to=room,skip_sid=request.sid)

@socketio.on_error_default
def default_error_handler(e):
    print("Error: {}".format(e))
    socketio.stop()

if __name__ == '__main__':
    socketio.run(app,host='127.0.0.1',port=9000)




