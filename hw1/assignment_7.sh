#!/bin/bash

if [[ $# -ne 1 ]]; then
	echo "Error: something went wrong"
	exit 1
fi

path=$1

if [[ -d $path ]]; then
	echo "It is a directory"
elif [[ -f $path ]]; then
	echo "It is a file"
else
	echo "File does not exist"
fi
