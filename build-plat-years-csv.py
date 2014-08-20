#!/usr/bin/env python
import lxml.html
import lxml.etree as etree

doc = lxml.html.parse('plat-index.html')
tables = doc.xpath('/html/body/table/tr/div/td/table')
main_table = tables[0]
#print([etree.tostring(x) for x in tables])

d = {}
rows = main_table.xpath('tr')[1:]
for row in rows:
    cols = row.xpath('td')

    year = int(cols[7].text)

    tile_url = cols[9].xpath('a/@href')[0]
    zipfn = tile_url.rsplit('/', 1)[1]
    trsid = zipfn.split('.')[0]

    d[trsid] = year

with open('plat-years.csv', 'w') as output:
    for trsid in sorted(d.keys()):
        year = d[trsid]
        output.write("{trsid},{year}\n".format(trsid=trsid, year=year))
