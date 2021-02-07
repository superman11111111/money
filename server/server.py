import requests
from settings import *
from etf import *
import json
import os
from flask import Flask, jsonify, request
import threading
import time
from datetime import datetime as dt

app = Flask(__name__)

etfs = [from_json(x) for x in json.loads(open('etfs.json', 'r').read())]
try:
    saves = os.listdir(TMP_DIR)
    for save in saves:
        tmpjj = json.loads(open(os.path.join(TMP_DIR, save), 'r').read())
        if tmpjj:
            etfsave = from_save(tmpjj)
            for i in range(len(etfs)):
                eetf = etfs[i]
                if eetf.name == etfsave.name:
                    etfs[i] = etfsave
except FileNotFoundError:
    pass
    

@app.route('/')
def index():
    return 'Hello'

@app.route('/dl')
def dl():
    for etf in etfs:
        etf.download()
    return index()

@app.route('/calc')
def ccalc():
    t = threading.Thread(target=_calc)
    t.start()
    return index()

@app.route('/alerts')
def alerts():
    d = request.args.get('d')
    if not d:
        d = 2
    else:
        d = int(d)
    r = []
    for etf in etfs:
        a = []
        alerts = etf.get_alerts(1)
        for tk, alert in alerts:
            if (dt.now() - dt.strptime(alert['date'][0], DTFORMAT)).days < d:
                a.append({'tk': tk, 'date': alert['date'][0], 'diff2mv': alert['diff2mv'][0]})
        a = sorted(a, key=lambda k: k['diff2mv']) 
        r.append({'name': etf.name, 'alerts': a})
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
        e = from_save(json.loads(open(os.path.join(TMP_DIR, f), 'r').read()))
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
    for etf in etfs:
        etf.mkdir()
    print(etfs)
    app.run(host=HOST, port=PORT, debug=DEBUG)



