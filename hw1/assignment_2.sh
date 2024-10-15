#!/bin/bash

file_path=$1
num_words=`wc -w < $file_path`
echo "Words count: $num_words" 
