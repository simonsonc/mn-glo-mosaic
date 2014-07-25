#!/usr/bin/env python
from osgeo import ogr
from osgeo import osr
from glob import glob
import os.path

driver = ogr.GetDriverByName("ESRI Shapefile")
ds = driver.CreateDataSource("cutline-map.shp")

srs = osr.SpatialReference()
srs.ImportFromEPSG(4326)

layer = ds.CreateLayer("tiles", srs, ogr.wkbPolygon)

field_name = ogr.FieldDefn("Name", ogr.OFTString)
field_name.SetWidth(16)
layer.CreateField(field_name)

for fn in glob("cutlines/*.json"):
    tile_id = os.path.splitext(os.path.basename(fn))[0]

    cutline_ds = ogr.Open(fn)
    cutline_layer = cutline_ds.GetLayerByIndex(0)
    cutline_feature = cutline_layer.GetNextFeature()
    while cutline_feature:
        poly = cutline_feature.GetGeometryRef().Clone()

        feature = ogr.Feature(layer.GetLayerDefn())
        feature.SetField("Name", tile_id)
        feature.SetGeometry(poly)

        layer.CreateFeature(feature)

        feature.Destroy()

        cutline_feature = cutline_layer.GetNextFeature()

ds.Destroy()
