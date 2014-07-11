def add_map(county, trs)
    outfn = "data/#{trs}"
    file outfn => 'data' do
        sh "wget 'ftp://ftp.lmic.state.mn.us/pub/data/basemaps/glo/#{county}/Georeferenced/#{trs}' -O#{outfn}"
    end
end

directory 'data'

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

multitask :download => download_tasks
county_tasks.each do |county, tasks|
    multitask county => tasks
end
