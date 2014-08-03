#!/bin/bash
for trsid; do
    rake data/${trsid}.zip
    gdal_translate -co TILED=YES -outsize 50% 50% /vsizip/data/${trsid}.zip/${trsid}.jpg ${trsid}.tif
    gdaladdo ${trsid}.tif 2 4 6 8 16
done
