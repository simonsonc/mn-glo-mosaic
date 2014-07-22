#!/usr/bin/env python
from osgeo import ogr
from osgeo import osr
from osgeo import gdal
import os.path

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
    for ext in raster_extents(outline):
        fn, _ = os.path.splitext(os.path.basename(outline))
        vrt = 'data/%s.vrt' % (fn,)
        extents[vrt] = ext

for x1 in range(460000, 520000, 10000):
    for y1 in range(4920000, 4970000, 10000):
        left = x1
        top = y1
        right = x1 + 10000
        bottom = y1 + 10000

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
            if not v.Disjoint(cutline):
                entries.append(k)

        print("%d %d (%d)" % (x1, y1, len(entries)))
        if len(entries):
            with open('tile-entries/%dx%d.txt' % (x1, y1), 'w') as out:
                for i in entries:
                    out.write(i + '\n')
