#!/usr/bin/env python
from osgeo import ogr
from osgeo import osr
from osgeo import gdal
import os.path
import os
import shutil

STEP = 10000
MINX = 180000 #189774.764105
MINY = 4810000 #4816337.325688
MAXX = 770000 #761944.028930
MAXY = 5480000 #5472405.931701

shutil.rmtree('tile-entries', True)
os.mkdir('tile-entries')

t_srs = osr.SpatialReference()
t_srs.ImportFromEPSG(26915)

s_ds = ogr.Open('cutline-map.shp')
s_layer = s_ds.GetLayerByIndex(0)

for x1 in range(MINX, MAXX, STEP):
    for y1 in range(MINY, MAXY, STEP):
        left = x1
        top = y1
        right = x1 + STEP
        bottom = y1 + STEP

        edge = ogr.Geometry(ogr.wkbLinearRing)
        edge.AssignSpatialReference(t_srs)
        edge.AddPoint(left, top)
        edge.AddPoint(right, top)
        edge.AddPoint(right, bottom)
        edge.AddPoint(left, bottom)
        edge.CloseRings()

        cutline = ogr.Geometry(ogr.wkbPolygon)
        cutline.AddGeometry(edge)

        s_layer.SetSpatialFilter(cutline)

        entries = sorted(set([feature.GetField('trsid') for feature in s_layer]))

        if len(entries):
            print("%d %d (%d)" % (x1, y1, len(entries)))
            with open('tile-entries/%dx%d.txt' % (x1, y1), 'w') as out:
                for i in entries:
                    out.write(i + '\n')
