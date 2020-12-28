#!/usr/bin/python
import sys
import json

topic=sys.argv[1]
tarray = { "topics": [{ "topic": topic }], "version":1 }

out = topic+'.json'
with open(out, 'w') as json_file:
    json.dump(tarray, json_file)

