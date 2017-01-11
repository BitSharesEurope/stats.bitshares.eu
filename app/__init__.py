import datetime
import os
import pygal
from flask import Flask, render_template, request, redirect, url_for
from .database import session, BTSBlock, TestBlock, SteemBlock, session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
rootpath = os.path.dirname(os.path.abspath(__file__))


@app.route('/')
def index():
    return render_template('index.html', **locals())

def plot(blocks):
    chart = pygal.Line()
    chart.x_labels = map(str, [
        datetime.datetime.fromtimestamp(b.timestamp) for b in blocks
    ])
    chart.add('Transactions', [b.num_txs for b in blocks])
    chart.add('Operations', [b.num_ops for b in blocks])
    return chart.render_response()


@app.route('/charts/steem')
def steem():
    blocks = session.query(SteemBlock).all()
    return plot(blocks)


@app.route('/charts/bitshares')
def bitshares():
    blocks = session.query(BTSBlock).all()
    return plot(blocks)


@app.route('/charts/testnet')
def testnet():
    blocks = session.query(TestBlock).all()
    return plot(blocks)
