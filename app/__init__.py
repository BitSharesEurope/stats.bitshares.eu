import json
import time
from .config import config
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit, join_room, leave_room
from sqlalchemy import func, desc
from statistics import mean

# from gevent import monkey
# monkey.patch_all()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(
    app,
    message_queue='redis://'
)

app.config['SQLALCHEMY_DATABASE_URI'] = config["sql_database"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

rooms = ['bts', 'gph', 'test']
namespace = "/status"


@app.before_first_request
def before_first_request():
    try:
        db.create_all()
    except Exception as e:
        app.logger.warning(str(e))


def log(msg):
    for room in rooms:
        socketio.emit(
            'log',
            {"msg": msg},
            namespace=namespace,
            room=room,
            broadcast=True)


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
    from .database import BTSBlock, TestBlock, SteemBlock

    # Leave all rooms!
    for r in rooms:
        leave_room(r)

    # Join only one room
    join_room(room)
    log("joined " + room)

    # Send all the stored data for that room
    if room == "bts":
        blocks = BTSBlock
    elif room == "test":
        blocks = TestBlock
    else:
        blocks = SteemBlock
    allblocks = [[
        b.timestamp,
        b.num_ops,
        b.num_txs,
        b.block_num
    ] for b in blocks.recent(1000)]
    socketio.emit(
        'init',
        sorted(allblocks, key=lambda x: x[0]),
        namespace=namespace,
        room=room,
        broadcast=True)


@socketio.on('stats', namespace='/status')
def on_stats(room):
    from .database import BTSBlock, TestBlock, SteemBlock
    # Send all the stored data for that room
    if room == "bts":
        blocks = BTSBlock
    elif room == "test":
        blocks = TestBlock
    else:
        blocks = SteemBlock
    query = db.session.query(
        func.max(blocks.num_ops).label("max_num_ops"),
        func.max(blocks.num_txs).label("max_num_txs"),
        func.sum(blocks.num_ops).label("sum_ops"),
        func.sum(blocks.num_ops).label("sum_txs"),
    ).first()

    last = (
        db.session.query(
            blocks.num_ops,
            blocks.num_txs
        )
        .order_by(blocks.timestamp.desc())
        .limit(100)
        .all()
    )

    socketio.emit(
        'stats',
        {
            "max_num_ops": int(query.max_num_ops),
            "max_num_txs": int(query.max_num_txs),
            "sum_ops": int(query.sum_ops),
            "sum_txs": int(query.sum_txs),
            "avg_ops_100": float(mean([x.num_ops for x in last])),
            "avg_txs_100": float(mean([x.num_txs for x in last])),
        },
        namespace=namespace,
        room=room,
        broadcast=True)
    

@socketio.on('leave', namespace='/status')
def on_leave(room):
    leave_room(room)


@app.errorhandler(404)
def page_not_found(e):
    return redirect("/", code=302)
