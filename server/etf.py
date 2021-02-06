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


class ETF():
    def __init__(self, name, link, dfs={}):
        self.name = name
        self.link = link
        self.dfs = dfs
        self.mkdir()

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

    def download(self, force=False):
        ct = rq.get(self.link).content
        # Get date from csv
        date = dt.strptime(ct[66:80].decode('utf-8').split(',')[0], '%m/%d/%Y')
        latest = self.dates()[-1]
        diff = (date - latest).days
        if force:
            diff = 1
        if diff == 0:
            print('no new data')
        elif diff > 0:
            self.mkdir()
            open(join(self.dir, self.fromDtf(date)+'.csv'), 'wb').write(ct)
            self.csv_to_dfs()
            self.calc()
        else:
            print('something went wrong')
            return 0
        return 1

    def update(self):
        pass

    def dates(self):
        l = [x.split('.csv')[0] for x in listdir(self.dir)] 
        l = [dt.strptime(x, DTFORMAT) for x in l]
        l.sort()
        return l

    def csv_to_dfs(self, n=0):
        '''
        n: convert last n dates (n=0 means all)
        '''
        import copy
        default = {'date': [], 'shares': [], 'market value($)': [], 'weight(%)': []}
        dates = listdir(self.dir)
        for i in range(len(dates)):
            date = dates[i]
            f = join(self.dir, date)
            tmp = pd.read_csv(f, delimiter=',')
            k = 0
            for j in range(len(tmp['ticker'])):
                tmptk = tmp['ticker'].iloc[j]
                if pd.isnull(tmptk):
                    continue
                tk = tmptk[:] 
                k+=1
                if tk not in self.dfs:
                    self.dfs[tk] = copy.deepcopy(default)
                for c in default.keys():
                    self.dfs[tk][c].append(tmp[c].iloc[j])

    def save(self):
        mkdir(TMP_DIR)
        open(join(TMP_DIR, self.name+'.json'), 'w').write(self.to_json())

    def calc(self):
        print(self)
        return
        self.csv_to_dfs()
        for tk in self.dfs:
            print(self.dfs[tk])
            for col in self.dfs[tk]:
                print(tk, col, len(self.dfs[tk][col]))
            df = pd.DataFrame(self.dfs[tk])
            df['date'] = pd.to_datetime(df['date'])
            df.index = df['date']
            df.sort_index(inplace=True)
            df['diff'] = df['shares'].diff()
            df['diff2mv'] = df['diff'].astype('float')/df['market value($)'].astype('float')
            df['date'] = df['date'].dt.strftime(DTFORMAT)
            df.index = list(range(len(df)))
            self.dfs[tk] = df.to_dict(orient='list')
        self.save()
        print(f'{self.name} saved!')
    
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
    return ETF(json['name'], json['link'])

def from_save(json):
    return ETF(json['name'], json['link'], json['dfs'])

