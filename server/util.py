import os
import pandas as pd
from datetime import datetime as dt
from settings import *

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

if __name__ == '__main__':
    check_labeling()

