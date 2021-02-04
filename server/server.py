import requests
from settings import *
import etf 
import json
import os
from flask import Flask
import threading

THREADS = []
etfs = [etf.from_json(x) for x in json.loads(open('etfs.json', 'r').read())]
print(etfs)

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello'

@app.route('/dl')
def dl():
    for etf in etfs:
        etf.download()
    return index()

@app.route('/calc')
def calc():
    for etf in etfs:
        etf.calc()
        return index()
    return index()

import time
def _observe():
    while 1:
        for etf in etfs:
            etf.download()
        time.sleep(60*60*6)

@app.route('/ob')
def observe():
    t = threading.Thread(target=_observe)
    global THREADS
    THREADS.append(t)
    print(THREADS)
    t.start()
    return index()

@app.route('/threads')
def threads():
    global THREADS
    import html
    return html.escape(str(THREADS))

@app.route('/info')
def info():
    global THREADS
    import html
    th = html.escape(str(threading.enumerate()))
    th += '<br>'
    th += '<br>'
    dirs = os.listdir(CSV_DIR)
    for d in dirs:
        th += d
        th += '<br>'
        th += html.escape(' '.join(sorted(os.listdir(os.path.join(CSV_DIR, d)))))
        th += '<br>'
        th += '<br>'
    return th


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=DEBUG)

