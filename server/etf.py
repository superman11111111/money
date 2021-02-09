import json
import requests as rq
from settings import *
from os.path import join
from os import listdir
from datetime import datetime as dt
from util import mkdir
import csv_formatter
import csv
import pandas as pd
import math


class MyETF:
    def __init__(self, name, link, cols, date_pos, dtformat, delimiter, decimal, csv_format, dfs=None):
        self.name = name
        self.link = link
        self.cols = cols
        self.date_pos = date_pos
        self.dtformat = dtformat
        self.delimiter = delimiter
        self.decimal = decimal
        self.csv_format = csv_format
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
        self.mkdir()
        ct = rq.get(self.link).content
        # Get date from csv
        self.date_pos = [int(x) for x in self.date_pos]
        date = dt.strptime(ct[self.date_pos[0]:self.date_pos[1]].decode('utf-8').split(',')[0], self.dtformat)
        latest = self.dates()
        if latest:
            diff = (date - latest[-1]).days
        else:
            diff = 1
        if force:
            diff = 1
        if diff == 0:
            self.print('no new data')
        elif diff > 0:
            ct = csv_formatter.parse(ct, self.csv_format)
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
        import numpy as np
        dates = listdir(self.dir)
        for i in range(len(dates)):
            date = dates[i]
            date_str = date.split('.csv')[0]
            f = join(self.dir, date)
            tmp = pd.read_csv(f, delimiter=self.delimiter, decimal=self.decimal)
            replace_columns = {}
            for col in self.cols:
                replace_columns[self.cols[col]] = col
            tmp = tmp.rename(columns=replace_columns)
            for j in range(len(tmp['ticker'])):
                tmptk = tmp['ticker'].iloc[j]
                if pd.isnull(tmptk):
                    continue
                tk = tmptk[:] 
                if tk not in self.dfs.keys():
                    self.dfs[tk] = {'date': []}
                    for col in list(self.cols.keys()):
                        if col == 'ticker':
                            continue 
                        self.dfs[tk][col] = []
                for k in self.dfs[tk]: 
                    if k == 'date':
                        v = date_str
                    else:
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
            df['diff'] = df['diff'].astype('float')
            try:
                df['market_value'] = df['market_value'].astype('float')
            except ValueError as e:
                df['market_value'] = [x.replace(',','') for x in df['market_value']]
            df['diff2mv'] = df['diff']/df['market_value']
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
    return MyETF(json['name'], json['link'], json['cols'], json['date_pos'], json['dtformat'], json['delimiter'], json['decimal'], json['csv_formatter'])

def from_save(json):
    return MyETF(json['name'], json['link'], json['cols'], json['dfs'])

