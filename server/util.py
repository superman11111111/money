import os
import pandas as pd
from datetime import datetime as dt
from settings import *
import etf

def mkdir(path):
    try:
        os.mkdir(path)
    except:
        pass

def check_labeling():
    e = 0
    for etf in os.listdir(CSV_DIR):
        for date in os.listdir(os.path.join(CSV_DIR, etf)):
            df = pd.read_csv(os.path.join(CSV_DIR, etf, date))
            dd = dt.strptime(date.split('.csv')[0], DTFORMAT)
            pp = dt.strptime(df['date'].iloc[0], '%m/%d/%Y')
            if (dd != pp):
                e += 1
                print(etf, date)
    if e == 0:
        print('No errors!')

def testing():
    etfs = []
    for i in range(5):
        etfs.append(etf.MyETF(f'{i}-etf', 'link', {}))
    etfs[0].dfs['TSLA'] = {}
    print(etfs)


if __name__ == '__main__':
    testing()

