import json
import requests as rq
from settings import *
from os.path import join
from os import listdir
from datetime import datetime as dt
from util import mkdir
import csv
import pandas as pd
import math


class MyETF:
    def __init__(self, name, link, dfs=None):
        self.name = name
        self.link = link
        if dfs is None:
            self.dfs = {}
        else:
            self.dfs = dfs

    def to_json(self):
        r = self.__dict__ 
        return json.dumps(r)

    def __repr__(self):
        return f'<{self.name} {len(list(self.dfs.keys()))} tks>'

    def mkdir(self):
        self.dir = join(CSV_DIR, self.name)
        mkdir(self.dir)

    def fromDtf(self, date):
        return dt.strftime(date, DTFORMAT)

    def toDtf(self, dstring):
        return dt.strptime(dstring, DTFORMAT)

    def print(self, msg):
        print(f'{self.name} {msg}')

    def download(self, force=False):
        ct = rq.get(self.link).content
        # Get date from csv
        date = dt.strptime(ct[66:80].decode('utf-8').split(',')[0], '%m/%d/%Y')
        latest = self.dates()[-1]
        diff = (date - latest).days
        if force:
            diff = 1
        if diff == 0:
            self.print('no new data')
        elif diff > 0:
            self.mkdir()
            open(join(self.dir, self.fromDtf(date)+'.csv'), 'wb').write(ct)
            self.calc()
        else:
            self.print('something went wrong')
            return 0
        return 1

    def update(self):
        pass

    def dates(self):
        l = [x.split('.csv')[0] for x in listdir(self.dir)] 
        l = [dt.strptime(x, DTFORMAT) for x in l]
        l.sort()
        return l

    def csv_to_dfs(self):
        '''
        n: convert last n dates (n=0 means all)
        '''
        import copy
        import numpy as np
        default = {'date': [], 'shares': [], 'market value($)': [], 'weight(%)': []}
        keys = list(default.keys())
        dates = listdir(self.dir)
        for i in range(len(dates)):
            date = dates[i]
            f = join(self.dir, date)
            tmp = pd.read_csv(f, delimiter=',')
            for j in range(len(tmp['ticker'])):
                tmptk = tmp['ticker'].iloc[j]
                if pd.isnull(tmptk):
                    continue
                tk = tmptk[:] 
                if tk not in self.dfs.keys():
                    self.dfs[tk] = copy.deepcopy(default) 
                if date.split('.csv')[0] in self.dfs[tk]['date']:
                    continue
                for k in self.dfs[tk]: 
                    try: 
                        v = tmp[k].iloc[j]
                    except KeyError:
                        v = np.nan
                    self.dfs[tk][k].append(v)

    def save(self):
        mkdir(TMP_DIR)
        open(join(TMP_DIR, self.name+'.json'), 'w').write(self.to_json())
        self.print('saved!')

    def calc(self):
        self.csv_to_dfs()
        for tk in self.dfs.keys():
            try:
                df = pd.DataFrame(self.dfs[tk])
            except ValueError:
                return
            df['date'] = pd.to_datetime(df['date'])
            df.index = df['date']
            df.sort_index(inplace=True)
            df['diff'] = df['shares'].diff()
            df['diff2mv'] = df['diff'].astype('float')/df['market value($)'].astype('float')
            df['date'] = df['date'].dt.strftime(DTFORMAT)
            df.index = list(range(len(df)))
            self.dfs[tk] = df.to_dict(orient='list')
        self.print('calculated')
        self.save()
    
    def get_alerts(self, n=5):
        alerts = []
        try:
            for tk in self.dfs:
                df = pd.DataFrame(self.dfs[tk])
                lastn = df[-n:]
                lastn = lastn.loc[lastn['diff2mv'] != 0]
                lastn = lastn.loc[lastn['diff2mv'].notna()]
                if not lastn.empty:
                    alerts.append([tk, lastn.to_dict(orient='list')])
        except:
            return 0
        return alerts 

def from_json(json):
    return MyETF(json['name'], json['link'])

def from_save(json):
    return MyETF(json['name'], json['link'], json['dfs'])

