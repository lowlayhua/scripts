#!/usr/bin/python
import sys
import os
import json

#-----------------------------------------------------------------------------------------
#broker_id = 0
#dest_dir = "/data8/kafka"
#-----------------------------------------------------------------------------------------
file=sys.argv[1]
broker=sys.argv[2]
broker_id=int(broker)
dest=sys.argv[3]
dest_dir="/"+dest+"/kafka"

print ("DEST",dest_dir)

with open(file, 'r') as f:
  array = json.load(f)
#  print(array)
  topic = array['topic']
  partition = array['partition']
  replica = array['replicas']
  spartition = str(partition)
  path = topic+'-'+spartition
  f.close()

count = 0
for id in array['replicas']:
  if id == broker_id:
     print(id)
     array['log_dirs'][count] = dest_dir
  else:
     array['log_dirs'][count] = "any"
  count = count + 1

topic2move = {"partitions": [{"topic": topic, "partition": partition, "log_dirs": array['log_dirs'], "replicas" : replica}]}
work_dir = "OUT"
ext =".json"
con_file = path+ext
slash = "/"
out = work_dir+slash+con_file
print(topic2move)
with open(out, 'w') as json_file:
    json.dump(topic2move, json_file)
