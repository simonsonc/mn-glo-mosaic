#!/usr/bin/env python
from osgeo import ogr
from osgeo import osr
import os
import os.path
import shutil

shutil.rmtree('cutlines', True)
os.mkdir('cutlines')

t_srs = osr.SpatialReference()
t_srs.ImportFromEPSG(26915)

features = {}
ds = ogr.Open('cutline-map.shp')
layer = ds.GetLayerByIndex(0)

t_driver = ogr.GetDriverByName('GeoJSON')

for feature in layer:
    trsid  = feature.GetField('trsid')
    features[trsid] = features.get(trsid, []) + [feature]

for trsid, feats in features.iteritems():
    t_ds = t_driver.CreateDataSource("cutlines/{0}.geojson".format(trsid))
    t_layer = t_ds.CreateLayer('tiles', t_srs, ogr.wkbPolygon)

    field_trsid = ogr.FieldDefn('trsid', ogr.OFTString)
    field_trsid.SetWidth(16)
    t_layer.CreateField(field_trsid)

    for feature in feats:
        t_feature = ogr.Feature(t_layer.GetLayerDefn())
        t_feature.SetGeometry(feature.GetGeometryRef())
        t_feature.SetField('trsid', trsid)

        t_layer.CreateFeature(t_feature)

    t_ds.Destroy()
