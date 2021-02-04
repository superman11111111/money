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
    def __init__(self, name, link):
        self.name = name
        self.link = link
        self.dfs = {}
        self.mkdir()

    def to_json(self):
        return json.dumps(self.__dict__)

    def __repr__(self):
        return f'<{self.name}>'

    def mkdir(self):
        self.dir = join(CSV_DIR, self.name)
        mkdir(self.dir)

    def download(self):
        ct = rq.get(self.link).content
        # Convert date to DTFORMAT
        date = dt.strptime(ct[66:80].decode('utf-8').split(',')[0], '%m/%d/%Y')
        date = dt.strftime(date, DTFORMAT)
        self.mkdir()
        open(join(self.dir, date+'.csv'), 'wb').write(ct)
        return 1

    def csv_to_dfs(self):
        import copy
        default = {'date': [], 'shares': [], 'market value($)': [], 'weight(%)': []}
        for date in listdir(self.dir):
            f = join(self.dir, date)
            tmp = pd.read_csv(f, delimiter=',')
            for i in range(len(tmp['ticker'])):
                tk = tmp['ticker'].iloc[i]
                if pd.isnull(tmp['ticker'][i]):
                    continue
                if tk not in self.dfs:
                    self.dfs[tk] = copy.deepcopy(default)
                for c in default.keys():
                    self.dfs[tk][c].append(tmp[c].iloc[i])

    def calc(self):
        self.csv_to_dfs()
        for tk in self.dfs:
            df = pd.DataFrame(self.dfs[tk])
            print(tk, df['shares'].diff())

def from_json(json):
    return ETF(json['name'], json['link'])

