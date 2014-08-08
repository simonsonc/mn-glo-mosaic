#!/usr/bin/env python3
from ftplib import FTP
import re

excluded = [x.strip() for x in open('bad-zip-names.txt').readlines()]
counties = [x.strip() for x in open('counties.txt').readlines()]

conn = FTP('ftp.lmic.state.mn.us')
conn.login()

filter_regex = re.compile('.*[fh][ic]0.\.zip')

for county in counties:
    print(county)

    conn.cwd('/pub/data/basemaps/glo/{county}/Georeferenced/'.format(county=county))

    zips = [x for x in conn.nlst() if x.endswith('.zip')]
    fizips = [x for x in zips if filter_regex.match(x)]
    final = [x for x in fizips if x not in excluded]

    with open('counties/{county}.txt'.format(county=county), 'wt') as out:
        for x in final:
            out.write(x + '\n')
