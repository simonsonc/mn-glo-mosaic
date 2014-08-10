#!/bin/sh
gdal_rasterize -burn 255 -burn 0 -burn 255 -l cutline-map -tr 2000 2000 -ot Byte cutline-map.shp problem-map.tif
