#!/bin/bash
bn=`basename $1`
trsid=${bn%%.*}
gdal_translate /vsizip/$1/${trsid}.jpg ${trsid}.tif
gdaladdo ${trsid}.tif 2 4 6 8 16
