require 'tempfile'

def safe_file(*args, &block)
    file(*args) do |t|
        begin
            yield
        rescue Exception => e
            rm t.name
            raise e
        end
    end
end

def add_map(county, trs)
    outfn = "data/#{trs}"
    safe_file outfn => 'data' do
        sh "wget 'ftp://ftp.lmic.state.mn.us/pub/data/basemaps/glo/#{county}/Georeferenced/#{trs}' -O#{outfn}"
    end
end

directory 'data'
directory 'tiled'

entries = {}
trs_by_county = Hash.new{|h,k| h[k] = []}
Dir.glob('counties/*.txt') do |fn|
    county = File.basename(fn, ".*")
    File.open(fn).each_line do |line|
        trs = line.strip
        trs_by_county[county] << File.basename(trs, ".*")
        entries[trs] = county
    end
end

download_tasks = []
county_tasks = Hash.new{|h,k| h[k] = []}
entries.each do |trs, county|
    task = add_map(county, trs)
    download_tasks << task
    county_tasks[county] << task
end

task :download => download_tasks
county_tasks.each do |county, tasks|
    task 'download:' + county => tasks
end

# Figure out what the problem zips are
problem_zips = File.open('problem-zips.txt').each_line.collect { |i| i.strip }

# Tasks for making the VRT file from the zip with the cutline included
cutline_tasks = []
entries.each do |entry, county|
    trs = File.basename(entry, ".*")
    if problem_zips.include?(entry) then
        input = "problem-map.tif"
        input_vsi = input
    else
        input = "data/#{entry}"
        input_vsi = "/vsizip/#{input}/#{trs}.jpg"
    end
    output = "data/#{trs}.vrt"
    cutline = "cutlines/#{trs}.geojson"

    task = safe_file output => [input, cutline] do
        sh "gdalwarp --config GDAL_CACHEMAX 1000 -of VRT -cutline '#{cutline}' -crop_to_cutline -dstalpha -overwrite '#{input_vsi}' '#{output}'"
    end
    cutline_tasks << task
end
task "cut:all" => cutline_tasks

# Tasks for building the VRT for things we already have downloaded
zips = FileList['data/t*.zip']

downloaded_fns = []
zips.each do |input|
    trs = File.basename(input, ".*")
    vrt = "data/#{trs}.vrt"
    downloaded_fns << vrt
end

task "cut:downloaded" => downloaded_fns

# Tile tasks
tiles = Hash.new{|h,k| h[k] = []}
FileList['tile-entries/*.txt'].each do |fn|
    tileid = File.basename(fn, ".*")
    File.open(fn).each_line do |line|
        tiles[tileid] << line.strip
    end
end

all_tile_tiffs = []
tiles.each do |k, v|
    inputs = v.collect { |i| "data/#{i}.vrt" }
    tile_entry_fn = "tile-entries/#{k}.txt"
    output = "tiled/#{k}.tif"
    file output => inputs + ['tiled', tile_entry_fn] do |t|
        x1, y1 = k.split('x')
        x2 = x1.to_i + 10000
        y2 = y1.to_i + 10000
        tmpfh = Tempfile.new(['tmp-tile', '.tif'])
        tmpfh.close
        begin
            tmpfn = tmpfh.path
            sh *["gdalwarp", "--config", "GDAL_CACHEMAX", "1000", "-te", x1, y1, x2.to_s, y2.to_s] + inputs + [tmpfn]
            sh *["gdal_translate", "--config", "GDAL_CACHEMAX", "1000", "-co", "COMPRESS=JPEG", "-co", "TILED=YES", "-outsize", "3750", "3750", tmpfn, "tiled/#{k}.tif"]
        ensure
            tmpfh.unlink
        end
    end

    all_tile_tiffs << output
end

task "tile:all" => all_tile_tiffs

def invert_multimap(map)
    ret = Hash.new{|h,k| h[k] = []}
    map.each do |k, v|
        v.each do |i|
            ret[i] << k
        end
    end
    ret
end

tiles_by_id = invert_multimap(tiles)
trs_by_county.each do |county, trs_list|
    county_tiles = []
    trs_list.each { |i| county_tiles += tiles_by_id[i] }
    tile_fns = county_tiles.collect { |i| "tiled/#{i}.tif" }
    task county => tile_fns
end

task :default => "tile:all"

task 'refresh-tiles' do
    sh 'python refresh-cutlines.py'
    sh 'python refresh-tile-entries.py'
end
