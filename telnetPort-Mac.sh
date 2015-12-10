#!/bin/bash

#
# Author: Ken Wu
# 
# This script is to determinte who is listening on a given TCP port on Mac OS X?
#
# 
#

if [ "$#" -ne 1 ]; then
    echo Illegal number of parameters
    echo "Specifically, it takes three arguments: 1) port number"
    echo Example of usage: ./telnetPort-Mac.sh 8080
    exit 0
fi

lsof -n -i4TCP:$1 | grep LISTEN

