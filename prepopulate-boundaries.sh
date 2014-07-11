#!/bin/bash
if [ ! -e alt_mn.zip ]; then
    # this shapefile has all the TRS boundaries for MN
    wget 'http://www.geocommunicator.gov/shapefilesall/state/alt_mn.zip'
fi

mkdir -p boundaries

zips=`cat counties/*.txt | sort | uniq`
for i in $zips; do
    name=${i%%.*}
    args=`echo $name | sed -e 's/t\([[:digit:]]*\)r\([[:digit:]]*\)\([we]\)\([[:digit:]]\).*/\1 \2 \3 \4/'`
    read twp range ew meridian <<< $args

    range="0$range"
    meridian="0$meridian"
    ew=`echo $ew | tr [a-z] [A-Z]`

    if [ "$meridian" == '04' ]; then
        meridian='46'
    fi

    echo $i $twp $range $ew $meridian

    #query="'town' = '${twp}' AND 'range' = '${range}' AND 'rngdir' = '${ew}' AND 'primer' = '${meridian}'"
    #echo "$query"

    query="'town' = '${twp}' AND 'range' = '${range}' AND 'rngdir' = '${ew}'"
    select="label"
    ogr2ogr -select "$select" -where "$query" -f GeoJSON boundaries/$name.json /vsizip/alt_mn.zip/alt_MN/alt_twnshp.shp
done
