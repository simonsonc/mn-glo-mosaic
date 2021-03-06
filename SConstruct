env = Environment()

from glob import glob
import os.path

entries = {}
counties = {}
for fn in glob('counties/*.txt'):
    county = os.path.splitext(os.path.basename(fn))[0]
    for line in open(fn).readlines():
        trs = line.strip().split('.')[0]
        entries[trs] = county
        counties[county] = counties.get(county, []) + [trs]

for trs, county in entries.iteritems():
    zipfile = env.Command(
        "data/%s.zip" % (trs,),
        '',
        "wget 'ftp://ftp.lmic.state.mn.us/pub/data/basemaps/glo/%s/Georeferenced/%s.zip' -O$TARGET" % (county, trs)
        )

    cutline = env.File("cutlines/{trs}.geojson".format(trs=trs))

    vrtfile = env.Command("data/%s.vrt" % (trs,), zipfile,
        "gdalwarp --config GDAL_CACHEMAX 1000 -of VRT -cutline '{cutline}' -crop_to_cutline -dstalpha -overwrite '/vsizip/$SOURCE/{trs}.jpg' '$TARGET'".format(trs=trs, cutline=cutline))

tiles = {}
tiles_by_trsid = {}
for fn in glob('tile-entries/*.txt'):
    tileid = os.path.splitext(os.path.basename(fn))[0]
    for line in open(fn).readlines():
        trsid = line.strip()
        tiles[tileid] = tiles.get(tileid, []) + [trsid]
        tiles_by_trsid[trsid] = tiles_by_trsid.get(trsid, []) + [tileid]

for tileid, trs in tiles.iteritems():
    inputs = ['data/' + i + '.vrt' for i in trs]
    tile_entry_fn = "tile-entries/" + tileid + ".txt" 
    x1, y1 = [int(x) for x in tileid.split('x')]
    x2 = x1 + 10000
    y2 = y1 + 10000

    env.Command("tiled/{tileid}.tif".format(tileid=tileid),
        inputs + [tile_entry_fn],
        'echo $TARGET $SOURCES'
        )

for county, trsids in counties.iteritems():
    tiles = set()
    for trsid in trsids:
        tiles.update(tiles_by_trsid.get(trsid, []))
    env.Alias(county, ['tiled/{0}.tif'.format(x) for x in tiles])
