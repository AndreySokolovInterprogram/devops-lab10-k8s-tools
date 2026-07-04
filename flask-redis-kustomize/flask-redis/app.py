import time
import redis
from flask import Flask, make_response
import socket
import os

app = Flask(__name__)

# Переменные окружения
DB_HOST = os.environ.get('REDIS_HOST', 'redis')
MY_ENV = os.environ.get('ENV', 'unknown')

cache = redis.Redis(host=DB_HOST, port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return int(cache.get('hits') or 0)
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

def incr_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/metrics')
def metrics():
    metrics = f'''# HELP view_count Flask-Redis-App visit counter
# TYPE view_count counter
view_count{{service="Flask-Redis-App"}} {get_hit_count()}
'''
    response = make_response(metrics, 200)
    response.mimetype = "text/plain"
    return response

@app.route('/')
def hello():
    incr_hit_count()
    count = get_hit_count()
    return 'Hello World! I have been seen {} times. My name is: {}. My env: {}\n'.format(
        count, socket.gethostname(), MY_ENV)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
