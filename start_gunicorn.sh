#!/bin/bash
gunicorn --worker-class eventlet -w 1 app:app -b 127.0.0.1:5000
