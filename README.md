# Money maker (Dollar dollar cash $$$)

### Game plan:

Get ARK ETF Portfolio, record changes, serve their biggest investments as API, acccess per App => Buy in broker (TradeRepublic)

### Step 1 (S1): Get Portfolio

Server Side: 

* csv/ folder structure: 

csv/
  |-- <Etf-name>
      |-- <date>.csv

### S2: Calculate changes in respect to market cap of stock

Math ;-;

ARKK = {'$NICE': <df>, ...}

$NICE
date sh  mv
9/11 100 $1M 
9/12 120 $2M
...

<df> = {'date': [], 'sh': [], ...}

some stocks only appear once, will maybe fill as time goes on

sort dates 

diff2mv = diff / mv


### S2.5: Query portfolios recurringly and put changes into system

Need some kind of state management, so I dont recalculate everything everytime a new entry follows

Skipping for now...


### S3: Serve as JSON Api 

Endpoints: 

/alerts : Get alerts of last day



### S4: Build small app to access (flutter)

