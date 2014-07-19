from osgeo import ogr
from osgeo import gdal

def GetExtent(gt,cols,rows):
    ''' Return list of corner coordinates from a geotransform

        @type gt:   C{tuple/list}
        @param gt: geotransform
        @type cols:   C{int}
        @param cols: number of columns in the dataset
        @type rows:   C{int}
        @param rows: number of rows in the dataset
        @rtype:    C{[float,...,float]}
        @return:   coordinates of each corner
    '''
    ext=[]
    xarr=[0,cols]
    yarr=[0,rows]

    for px in xarr:
        for py in yarr:
            x=gt[0]+(px*gt[1])+(py*gt[2])
            y=gt[3]+(px*gt[4])+(py*gt[5])
            ext.append([x,y])
        yarr.reverse()
    return ext

def raster_extents(raster):
    ds=gdal.Open(raster)

    gt=ds.GetGeoTransform()
    cols = ds.RasterXSize
    rows = ds.RasterYSize
    ext=GetExtent(gt,cols,rows)
    return ext

def contained(ext, x1, y1):
    mx1 = min(ext[0][0], ext[1][0], ext[2][0], ext[3][0])
    mx2 = max(ext[0][0], ext[1][0], ext[2][0], ext[3][0])
    my1 = min(ext[0][1], ext[1][1], ext[2][1], ext[3][1])
    my2 = max(ext[0][1], ext[1][1], ext[2][1], ext[3][1])

    x2, y2 = x1 + 10000, y1 + 10000
    ret = not (x2 < mx1 or x1 > mx2 or y2 < my1 or y1 > my2)
    return ret

extents = {}
import glob
for vrt in glob.glob('data/*.vrt'):
    ext = raster_extents(vrt)
    if ext:
        extents[vrt] = ext

for x1 in range(460000, 520000, 10000):
    for y1 in range(4920000, 4970000, 10000):
        entries = []
        print("%s %s" % (x1, y1))
        for k, v in extents.iteritems():
            if contained(v, x1, y1):
                entries.append(k)

        if len(entries):
            with open('tile-entries/%dx%d.txt' % (x1, y1), 'w') as out:
                for i in entries:
                    out.write(i + '\n')
