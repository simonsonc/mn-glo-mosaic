#!/bin/bash
trsid=$1
rake data/${trsid}.zip
gdal_translate /vsizip/data/${trsid}.zip/${trsid}.jpg ${trsid}.tif
gdaladdo ${trsid}.tif 2 4 6 8 16
