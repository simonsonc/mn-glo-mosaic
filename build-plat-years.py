#!/usr/bin/env python
from osgeo import ogr
from osgeo import osr
import csv

def get_years():
    ret = {}
    with open('plat-years.csv') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        for row in csvreader:
            ret[row[0]] = int(row[1])
    return ret

years = get_years()

t_driver = ogr.GetDriverByName("ESRI Shapefile")
t_fn = "summary-maps/plat-years.shp"
t_driver.DeleteDataSource(t_fn)
t_ds = t_driver.CreateDataSource(t_fn)

t_srs = osr.SpatialReference()
t_srs.ImportFromEPSG(26915)

t_layer = t_ds.CreateLayer("years", t_srs, ogr.wkbPolygon)

trsid_field = ogr.FieldDefn("trsid", ogr.OFTString)
trsid_field.SetWidth(16)
t_layer.CreateField(trsid_field)

year_field = ogr.FieldDefn("year", ogr.OFTInteger)
t_layer.CreateField(year_field)

s_ds = ogr.Open('cutline-map.shp')
s_layer = s_ds.GetLayerByIndex(0)

for s_feature in s_layer:
    trsid = s_feature.GetField('trsid')
    year = years[trsid]
    if year == 0:
        continue

    t_feature = ogr.Feature(t_layer.GetLayerDefn())
    t_feature.SetGeometry(s_feature.GetGeometryRef())
    t_feature.SetField('trsid', trsid)
    t_feature.SetField('year', year)

    t_layer.CreateFeature(t_feature)
