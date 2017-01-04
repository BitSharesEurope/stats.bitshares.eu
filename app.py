from app import socketio as io, app

if __name__ == '__main__':
    io.run(app, debug=True)
