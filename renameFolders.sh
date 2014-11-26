#!/bin/bash

#
# Author: Ken Wu
# 
# This script is to rename folders recursively.  
# Specifically, it takes three arguments: 1) starting directory, 2) old-occurence, 3) new-occurence.  It first removes all directories with new-occurence and rename all directories from old-occurence to new-occurene
#
# 
#

if [ "$#" -ne 3 ]; then
    echo "Illegal number of parameters"
    echo "Specifically, it takes three arguments: 1) starting directory, 2) old-occurence, 3) new-occurence.  It first removes all directories with new-occurence and rename all directories from old-occurence to new-occurene"
    echo "Example of usage: ./renameFolders.sh /home/ken/work/kenDoc 20141125 20141126"
    exit 0
fi

dirPath=$1
old=$2
new=$3

#remove the existing directories with new-occurence
find $1 -name "*$new*" -type d | xargs rm -rf

#move all directories from 'old-occurence' to 'new-occurence'
find $1 -name "*$old*" -type d | sed -e "p;s/$old/$new/g" | xargs -n2 mv
