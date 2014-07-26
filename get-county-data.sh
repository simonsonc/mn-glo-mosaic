#!/bin/bash
while read line
do
    echo $line
    #curl -l "ftp://ftp.lmic.state.mn.us/pub/data/basemaps/glo/$line/Georeferenced/" | grep '.*i[0-9][0-9]\.zip$' > "counties/$line.txt"
    curl -l "ftp://ftp.lmic.state.mn.us/pub/data/basemaps/glo/$line/Georeferenced/" | grep ".*01.zip$" > "counties/$line.txt"
done < counties.txt
