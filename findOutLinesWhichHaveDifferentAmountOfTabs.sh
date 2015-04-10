#!/bin/bash

#
# Author: Ken Wu
# 

export IFS="\n"
counts=`awk '{print gsub(/\t/,"")}' "$1"`
echo "$counts" > tmp.out
tabCount=-1
counter=1
while read p; do
	if [ "$tabCount" -eq -1 ]; then
		let tabCount="$p"
	else
		if [ "$tabCount" -ne "$p" ]; then
			echo "There is a line (i.e. line: $counter) which has different amount of tabs!!!"
			exit 1
		fi
	fi
	let counter=counter+1
done <tmp.out

rm tmp.out
echo "All lines have the same amount of tabs"

#for c in $counts; do
#	echo "$c ->"
#done
