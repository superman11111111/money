import json
import requests as rq
from settings import *
from os.path import join
from datetime import datetime as dt
from util import mkdir


class ETF():
    def __init__(self, name, link):
        self.name = name
        self.link = link

    def to_json(self):
        return json.dumps(self.__dict__)

    def __repr__(self):
        return f'<{self.name}>'

    def download(self):
        ct = rq.get(self.link).content
        # Convert date to DTFORMAT
        date = dt.strptime(ct[66:80].decode('utf-8').split(',')[0], '%m/%d/%Y')
        date = dt.strftime(date, DTFORMAT)

        f = join(CSV_DIR, self.name)
        mkdir(f)

        open(join(f, date+'.csv'), 'wb').write(ct)
        return 1

    def calc(self):
        
        pass 

def from_json(json):
    return ETF(json['name'], json['link'])

