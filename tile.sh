#!/bin/sh
for x in `seq 460000 10000 520000`; do
    for y in `seq 4920000 10000 4970000`; do
        x2=$((x + 10000))
        y2=$((y + 10000))
        echo $x $y $x2 $y2
        ref="${x}x${y}"
        entry_fn="tile-entries/${ref}.txt"
        if [ -e $entry_fn ]; then
            entries=`cat $entry_fn`
            #gdalwarp -te $x $y $x2 $y2 *.tif poop/${x}x${y}.tif
            #gdalwarp -co TILED=YES -co COMPRESS=JPEG -te $x $y $x2 $y2 trimmed/all.vrt tiled/${x}x${y}.tif
            gdalwarp -co TILED=YES -co COMPRESS=JPEG -te $x $y $x2 $y2 $entries tiled/${x}x${y}.tif
        fi
    done
done
