#!/usr/bin/env python
from osgeo import ogr
from osgeo import osr
from glob import glob
import os
import os.path
import re
import shutil

shutil.rmtree('boundaries', True)
os.mkdir('boundaries')

t_srs = osr.SpatialReference()
t_srs.ImportFromEPSG(26915)

def get_zips():
    for fn in glob('counties/*.txt'):
        for line in open(fn).readlines():
            yield line.strip()

name_regex = re.compile(r't(\d+)r(\d+)([we])(\d).*')

features = {}
ds = ogr.Open('/vsizip/trs.zip/tr.shp')
layer = ds.GetLayerByIndex(0)

t_driver = ogr.GetDriverByName('GeoJSON')

for feature in layer:
    twp = feature.GetField('TOWN')
    rang = feature.GetField('RANG')
    ew = 'w' if feature.GetField('DIR') == 2 else 'e'
    featid = (twp, rang, ew)

    features[featid] = features.get(featid, []) + [feature]

zips = set(get_zips())
for i in zips:
    trsid = os.path.splitext(i)[0]
    twp, rng, ew, meridian = name_regex.match(trsid).groups()
    featid = (int(twp), int(rng), ew)

    t_ds = t_driver.CreateDataSource("boundaries/{0}.geojson".format(trsid))
    t_layer = t_ds.CreateLayer('tiles', t_srs, ogr.wkbPolygon)

    field_trsid = ogr.FieldDefn('trsid', ogr.OFTString)
    field_trsid.SetWidth(16)
    t_layer.CreateField(field_trsid)

    for feature in features[featid]:
        t_feature = ogr.Feature(t_layer.GetLayerDefn())
        t_feature.SetGeometry(feature.GetGeometryRef())
        t_feature.SetField('trsid', trsid)

        t_layer.CreateFeature(t_feature)

    t_ds.Destroy()
