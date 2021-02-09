import json
import etf

etfs = json.loads(open('etfs.json', 'r').read())

def main():
    print('Choose ETF')
    print('(0) All')
    for i in range(len(etfs)):
        print(f'({i+1}) {etfs[i]["name"]}')

    sel = int(input(f'(0-{len(etfs)}): '))
    if sel == 0:
        for e in etfs:
            myetf = etf.from_json(e)
            test(myetf)
    elif sel <= len(etfs):
        test(etf.from_json(etfs[sel-1]))
    else:
        print('Abort.')

def test(myetf):
    myetf.download()

if __name__ == '__main__':
    main()

