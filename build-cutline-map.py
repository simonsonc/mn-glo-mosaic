#!/usr/bin/env python
from osgeo import ogr
from osgeo import osr
from glob import glob
import os.path

driver = ogr.GetDriverByName("ESRI Shapefile")
ds = driver.CreateDataSource("summary-maps/cutline-map.shp")

srs = osr.SpatialReference()
srs.ImportFromEPSG(26915)

cutline_srs = osr.SpatialReference()
cutline_srs.ImportFromEPSG(4326)

coord_trans = osr.CoordinateTransformation(cutline_srs, srs)

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
        poly.Transform(coord_trans)

        feature = ogr.Feature(layer.GetLayerDefn())
        feature.SetField("Name", tile_id)
        feature.SetGeometry(poly)

        layer.CreateFeature(feature)

        feature.Destroy()

        cutline_feature = cutline_layer.GetNextFeature()

ds.Destroy()
