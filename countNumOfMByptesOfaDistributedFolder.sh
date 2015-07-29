#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters"
    echo "Specifically, it takes one argument: 1) A remote s3 or hdfs path"
    echo "Example of usage: ./countNumOfMByptesOfaDistributedFolder.sh s3n://xxxx/yyy/zzz"
    exit 0
fi

s=`hadoop fs -du "$1" | cut -d " " -f 1 | awk '{ sum += $0 } END { print sum }'`
echo "There are $((s/(1024*1024))) mega bytes ($s byptes) in the $1 folder."
