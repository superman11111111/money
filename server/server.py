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

@app.route('/alerts')
def alerts():
    print('alerts')
    d = request.args.get('d')
    if not d:
        d = 2
    else:
        d = int(d)
    b = request.args.get('b')
    if not b:
        b = .001
    else:
        b = float(b)
    r = []
    for etf in etfs:
        a = []
        alerts = etf.get_alerts(d)
        alerts = [alert for alert in alerts if (dt.now()-dt.strptime(alert['date'], DTFORMAT)).days<d]
        alerts = [alert for alert in alerts if abs(alert['diff2mv'])>b]
        alerts.sort(key=lambda k: k['diff2mv'])
        r.append({'etf': etf.name, 'alerts': alerts})
    return jsonify(r)

def _observe():
    time.sleep(3)
    for etf in etfs:
        etf.mkdir()
        etf.calc()
    while 1:
        print(f'[{dt.now()}]')
        for etf in etfs:
            etf.download()
        time.sleep(QUERY_INTERVAL)

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
    print('[SERVER]: INITIALIZATION')
    t = threading.Thread(target=_observe)
    t.start()
    if DEBUG:
        app.run(host=HOST, port=PORT)
    else:
        from waitress import serve
        serve(app, listen=f'{HOST}:{PORT}')



