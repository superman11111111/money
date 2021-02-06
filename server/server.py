import requests
from settings import *
import etf 
import json
import os
from flask import Flask, jsonify
import threading
import time
from datetime import datetime as dt

app = Flask(__name__)

try:
    saves = os.listdir(TMP_DIR)
    etfs = [etf.from_save(json.loads(open(os.path.join(TMP_DIR, x), 'r').read())) for x in saves]
except FileNotFoundError:
    etfs = [etf.from_json(x) for x in json.loads(open('etfs.json', 'r').read())]
    
print(etfs)

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
    t = threading.Thread(target=_calc)
    t.start()
    return index()

@app.route('/alerts')
def alerts():
    r = {}
    for etf in etfs:
        a = []
        alerts = etf.get_alerts(1)
        for tk, alert in alerts:
            if (dt.now() - dt.strptime(alert['date'][0], DTFORMAT)).days < 2:
                a.append({'tk': tk, 'date': alert['date'][0], 'diff2mv': alert['diff2mv'][0]})
        a = sorted(a, key=lambda k: k['diff2mv']) 
        r[etf.name] = a
    return jsonify(r)

def _calc():
    for etf in etfs:
        etf.calc()
    return 1

def _observe():
    while 1:
        for etf in etfs:
            etf.download(1)
        time.sleep(QUERY_INTERVAL)

@app.route('/save')
def save():
    for etf in etfs: 
        print(etf.latest())
        etf.save()
    return index()

@app.route('/load')
def load():
    for f in os.listdir(TMP_DIR):
        e = etf.from_save(json.loads(open(os.path.join(TMP_DIR, f), 'r').read()))
        print(e.dfs)
    return index()

@app.route('/ob')
def observe():
    t = threading.Thread(target=_observe)
    t.start()
    return index()

@app.route('/info')
def info():
    import html
    th = '<br>'.join([html.escape(str(x)) for x in threading.enumerate()])
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

