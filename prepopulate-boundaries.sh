#!/bin/bash
if [ ! -e trs.zip ]; then
    # this shapefile has all the TRS boundaries for MN
    wget 'ftp://ftp.lmic.state.mn.us/pub/data/admin_poli/trs.zip'
fi

mkdir -p boundaries

zips=`cat counties/*.txt | sort | uniq`
for i in $zips; do
    name=${i%%.*}
    args=`echo $name | sed -e 's/t\([[:digit:]]*\)r\([[:digit:]]*\)\([we]\)\([[:digit:]]\).*/\1 \2 \3 \4/'`
    read twp range ew meridian <<< $args

    twp=`echo $twp | sed -e "s/^0*//"`
    range=`echo $range | sed -e "s/^0*//"`
    meridian="0$meridian"
    if [ $ew == 'e' ]; then
        ew="1"
    else
        ew="2"
    fi

    if [ "$meridian" == '04' ]; then
        meridian='46'
    fi

    echo $i $twp $range $ew $meridian

    #query="'town' = '${twp}' AND 'range' = '${range}' AND 'rngdir' = '${ew}' AND 'primer' = '${meridian}'"
    #echo "$query"

    query="'TOWN' = '${twp}' AND 'RANG' = '${range}' AND 'DIR' = '${ew}'"
    select="TWP_LABEL"
    ogr2ogr -t_srs "EPSG:4326" -select "$select" -where "$query" -f GeoJSON boundaries/$name.json /vsizip/trs.zip/tr.shp

    # clean up
    sed -i -e '/^"crs"/d' boundaries/$name.json
    python reformat-json.py boundaries/$name.json
done
