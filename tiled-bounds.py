#!/usr/bin/env python
from osgeo import ogr
from osgeo import osr
from osgeo import gdal
import os.path

STEP = 10000
MINX = 180000 #189774.764105
MINY = 4810000 #4816337.325688
MAXX = 770000 #761944.028930
MAXY = 5480000 #5472405.931701

t_srs = osr.SpatialReference()
t_srs.ImportFromEPSG(26915)

s_srs = osr.SpatialReference()
s_srs.ImportFromEPSG(4326)

def raster_extents(raster):
    ds=ogr.Open(raster)

    layer=ds.GetLayerByIndex(0)
    left, right, top, bottom = layer.GetExtent()

    feature = layer.GetNextFeature()
    while feature:
        geom = feature.GetGeometryRef().Clone()
        geom.TransformTo(t_srs)
        yield geom

        feature = layer.GetNextFeature()

extents = {}
import glob
for outline in glob.glob('cutlines/*.json'):
    fn, _ = os.path.splitext(os.path.basename(outline))
    extents[fn] = list(raster_extents(outline))

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

        entries = []
        for k, v in extents.iteritems():
            #print("Edge", str(cutline))
            #print("V", str(v))
            if any([not x.Disjoint(cutline) for x in v]):
                entries.append(k)

        if len(entries):
            print("%d %d (%d)" % (x1, y1, len(entries)))
            with open('tile-entries/%dx%d.txt' % (x1, y1), 'w') as out:
                for i in entries:
                    out.write(i + '\n')
