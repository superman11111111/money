import os
import json
import etf 

etfs = json.loads(open('etfs.json', 'r').read())


sel = int(input('(0) ADD\n(1) EDIT\n(0-1): '))
if sel == 0:
    name = input('Name: ')
    link = input('Link: ')
    columns = input('Columns (col1, col2, ...): ').split(', ')
    date_pos = [int(x) for x in input('Date pos (pos1, pos2): ').split(', ')]
    etfs.append({'name': name, 'link': link, 'cols': columns, 'date_pos': date_pos})
elif sel == 1:
    print('Choose ETF')
    print('(0) All')
    for i in range(len(etfs)):
        print(f'({i+1}) {etfs[i]["name"]}')

    enum = int(input(f'(0-{len(etfs)}): '))
    if enum <= len(etfs):
        if enum == 0:
            # Only add no edit
            new_key = input('New Key name: ')
            new_value = input(f'New Value for {new_key}: ')
            formats = [int, str, list]
            print(f'Format of {new_value}: ')
            for i in range(len(formats)):
                print(f'({i}) {formats[i]}')
            findex = int(input(f'(0-{len(formats)-1}): '))
            if formats[findex] == list:
                new_value = new_value.split(', ')
            else:
                new_value = formats[findex](new_value)
            for et in etfs:
                et[new_key] = new_value
        else:
            sel2 = int(input('(0) ADD\n(1) EDIT\n(2) EDIT ALL\n(0-2): '))
            if sel2 == 0:
                new_key = input('New Key name: ')
                new_value = input(f'New Value for {new_key}: ')
                etfs[enum-1][new_key] = new_value
            elif sel2 == 1:
                et = etfs[enum-1]
                keys = list(et.keys())
                for i in range(len(keys)):
                    print(f'({i}) {keys[i]}')
                attr = int(input(f'(0-{len(keys)}): '))
                if attr <= len(keys):
                    key = keys[attr]
                    types = [int, str, list]
                    for ty in types:
                        if isinstance(et[key], ty):
                            if ty == list:
                                et[key] = input(f'New value for {key} (v1, v2,...): ').split(', ')
                            else:
                                etfs[key] = ty(input(f'New value for {key}({ty}): '))
                    etfs[enum-1] = et
            elif sel2 == 2:
                keys = list(etfs[enum-1].keys())
                for key in keys:
                    types = [int, str, list]
                    for ty in types:
                        if isinstance(etfs[enum-1][key], ty):
                            if ty == list:
                                etfs[enum-1][key] = input(f'New value for {key} (v1, v2,...): ').split(', ')
                            else:
                                etfs[enum-1][key] = ty(input(f'New value for {key}({ty}): '))

else:
    print('Abort.')
    quit()
        
    
open('etfs.json', 'w').write(json.dumps(etfs))
