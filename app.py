#!/usr/bin/env python

import json
import time
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, message_queue='redis://')

rooms = ['bts' , 'gph', 'test']


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('my event', namespace='/status')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': message['data'], 'count': session['receive_count']})


@socketio.on('my broadcast event', namespace='/status')
def test_broadcast_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': message['data'], 'count': session['receive_count']},
         broadcast=True)


@socketio.on('connect', namespace='/status')
def test_connect():
    emit('my response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect', namespace='/status')
def test_disconnect():
    print('Client disconnected', request.sid)


@socketio.on('join', namespace='/status')
def on_join(room):
    for r in rooms:
        leave_room(r)
    join_room(room)


@socketio.on('leave', namespace='/status')
def on_leave(room):
    leave_room(room)


if __name__ == '__main__':
    socketio.run(app, debug=True)
