#!/bin/bash

all_files=$@

for filename in $all_files
do
	if ! [[ -f $filename ]]; then
		echo "File $filename does not exist"
		exit 1
	fi
done

tar -cvzf tar.gz $all_files
