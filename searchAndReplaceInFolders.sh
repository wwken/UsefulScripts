#!/bin/bash

#
# Author: Ken Wu
# Date: July 06 2015
# 
# This script is to search for a given string and replace it with another string in the given folder recursively.  
# Specifically, it takes three arguments: 
# 1) starting directory, 
# 2) string-to-be-located, 
# 3) string-to-be-replaced
#
# For example, if we run: './searchAndReplaceInFolders.sh /server/config/ dev prod ', it is going to search all occurences of "dev" inside /server/config and replace it with "prod"
#

if [ "$#" -ne 3 ]; then
    echo "Illegal number of parameters"
    echo "Specifically, it takes three arguments: 1) starting directory, 2) old-occurence, 3) new-occurence.  It first removes all directories with new-occurence and rename all directories from old-occurence to new-occurene"
    echo "Example of usage: ./searchAndReplaceInFolders.sh /server/config/ dev prod"
    exit 0
fi

dirPath=$1
sOld=$2
sNew=$3

find $1 -type f -exec sed -i -e "s/$2/$3/g" {} \;