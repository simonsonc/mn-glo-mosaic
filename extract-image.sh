#!/bin/bash
bn=`basename $1`
trsid=${bn%%.*}
gdal_translate /vsizip/$1/${trsid}.jpg ${trsid}.tif
