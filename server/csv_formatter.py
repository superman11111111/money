def parse(ct, csv_format):
    l = csv_format.split(' ')
    if len(l) == 3:
        if l[0] == "REMOVE":
            if l[1] == "ROW":
                rows = l[2].split(',')
                ct = ct.decode('utf-8')
                ctl = ct.split('\n')
                for row in rows:
                    ctl[int(row)] = ''
                ctl = [l for l in ctl if l]
                ct = bytes('\n'.join(ctl), 'utf-8')
    return ct

