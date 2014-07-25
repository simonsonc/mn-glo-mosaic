#!/usr/bin/env python
from osgeo import ogr
from osgeo import osr
from glob import glob
import os

driver = ogr.GetDriverByName("ESRI Shapefile")
ds = driver.CreateDataSource("tile-map.shp")

srs = osr.SpatialReference()
srs.ImportFromEPSG(26915)

layer = ds.CreateLayer("tiles", srs, ogr.wkbPolygon)

field_name = ogr.FieldDefn("Name", ogr.OFTString)
field_name.SetWidth(16)
layer.CreateField(field_name)

tile_ids = [ os.path.splitext(os.path.basename(x))[0] for x in glob('tile-entries/*.txt') ]

for tile_id in tile_ids:
    x1_s, y1_s = tile_id.split('x')
    x1 = int(x1_s)
    y1 = int(y1_s)
    x2 = x1 + 10000
    y2 = y1 + 10000

    ring = ogr.Geometry(ogr.wkbLinearRing)
    ring.AddPoint(x1, y1)
    ring.AddPoint(x2, y1)
    ring.AddPoint(x2, y2)
    ring.AddPoint(x1, y2)
    ring.CloseRings()

    poly = ogr.Geometry(ogr.wkbPolygon)
    poly.AddGeometry(ring)

    feature = ogr.Feature(layer.GetLayerDefn())
    feature.SetField("Name", tile_id)
    feature.SetGeometry(poly)

    layer.CreateFeature(feature)

    feature.Destroy()

ds.Destroy()
