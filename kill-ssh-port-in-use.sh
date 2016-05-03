#!/bin/bash

#
# Author: Ken Wu
# 
# This script is to kill any ssh-port that are in use
#
# 	Usage:
#		./kill-ssh-port-in-use.sh 8157
#

PORT=$1

kill -9 $(lsof -n -i | grep $PORT | grep ssh | grep -v grep | awk '{print $2}');