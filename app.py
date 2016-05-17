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


@socketio.on('connect', namespace='/status')
def test_connect():
    print('Client connected', request.sid)


@socketio.on('disconnect', namespace='/status')
def test_disconnect():
    print('Client disconnected', request.sid)


@socketio.on('join', namespace='/status')
def on_join(room):
    # Leave all rooms!
    for r in rooms:
        leave_room(r)
    # Join only one room
    join_room(room)


@socketio.on('leave', namespace='/status')
def on_leave(room):
    leave_room(room)


if __name__ == '__main__':
    socketio.run(app, debug=True)
