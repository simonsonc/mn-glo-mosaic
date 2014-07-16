#!/usr/bin/env python
import sys
import json

for i in sys.argv[1:]:
    with open(i) as infile:
        data = json.load(infile)

    cleaned = json.dumps(data, sort_keys=False, indent=2) 

    with open(i, "w") as output:
        for line in cleaned.split('\n'):
            output.write(line.rstrip() + '\n')
