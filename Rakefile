def add_map(county, trs)
    outfn = "data/#{trs}"
    file outfn => 'data' do
        sh "wget 'ftp://ftp.lmic.state.mn.us/pub/data/basemaps/glo/#{county}/Georeferenced/#{trs}' -O#{outfn}"
    end
end

directory 'data'
directory 'trimmed'
directory 'tiled'

entries = {}
Dir.glob('counties/*.txt') do |fn|
    county = File.basename(fn, ".*")
    File.open(fn).each_line do |line|
        entries[line.strip] = county 
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

# Tasks for making the VRT file from the zip with the cutline included
zips = FileList['data/t*.zip']

cutline_tasks = []
zips.each do |input|
    trs = File.basename(input, ".*")
    output = "data/#{trs}.vrt"
    cutline = "cutlines/#{trs}.json"

    task = file output => [input, cutline] do
        sh "gdalwarp -of VRT -cutline '#{cutline}' -crop_to_cutline -dstalpha -overwrite '/vsizip/#{input}/#{trs}.jpg' '#{output}'"
    end
    cutline_tasks << task
end

task :cut => cutline_tasks

# Tasks for actually trimming the tiles
trim_tasks = []
trim_jpgs = []
zips.each do |input|
    trs = File.basename(input, ".*")
    output = "trimmed/#{trs}.jpg"
    trim_jpgs << output
    vrt = "data/#{trs}.vrt"
    task = file output => ['trimmed', vrt] do
        sh "gdal_translate -of JPEG '#{vrt}' '#{output}'"
    end
    trim_tasks << task
end

task :trim => trim_tasks

# Tasks for building the final patchwork
file 'trimmed/all.vrt' => trim_jpgs do |t|
    sh *["gdalbuildvrt", "trimmed/all.vrt"] + trim_jpgs
end
task :build => 'trimmed/all.vrt'

tiles = Hash.new{|h,k| h[k] = []}
FileList['tile-entries/*.txt'].each do |fn|
    tileid = File.basename(fn, ".*")
    File.open(fn).each_line do |line|
        tiles[tileid] << line.strip
    end
end

tiles.each do |k, v|
    inputs = v.collect { |i| "data/#{i}.vrt" }
    file "tiled/#{k}.tif" => inputs do |t|
        x1, y1 = k.split('x')
        x2 = x1.to_i + 10000
        y2 = y1.to_i + 10000
        sh *["gdalwarp", "-co", "TILED=YES", "-co", "COMPRESS=JPEG", "-te", x1, y1, x2.to_s, y2.to_s] + inputs + ["tiled/#{k}.tif"]
    end
end

task :default => :build
