#!/bin/bash

#-----------------------------------------------------------------------------------------
ZOOKEEPER="172.20.42.85"
BROKERLIST="0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32"
TOPIC=$1
P=$2
#-----------------------------------------------------------------------------------------

  INFILE=${TOPIC}.json
  echo "Generate ${INFILE}"
  /opt/confluent/bin/kafka-reassign-partitions --generate --zookeeper ${ZOOKEEPER}  --broker-list ${BROKERLIST} --topics-to-move-json-file ${INFILE} &> s2_${INFILE}

  echo "Generate s3_${INFILE}"
  head -2 s2_${INFILE} | tail -1  &> s3_${INFILE}
#  mv s2_${INFILE} current
#  rm ${INFILE}

  PINFILE=${TOPIC}-${P}.json
  echo "jq '.partitions[]| select( .partition == "${P}" )' s3_${INFILE} &> s4_${PINFILE}"
  jq '.partitions[]| select( .partition == '"${P}"' )' s3_${INFILE} &> s4_${PINFILE}
