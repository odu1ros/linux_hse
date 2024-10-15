#!/bin/bash

declare -a current_line
declare -a prev_line

number_lines=$1
if [[ $# -eq 0 ]]; then
	number_lines=5
else
	if ! [[ $number_lines =~ ^[0-9]+$ ]]; then
		echo "Error: you should use a positive integer as an argument"
		exit 1
	fi
fi

for((i=0;i<$number_lines;i++))
do
	current_line=()
	current_line[0]=1
	current_line[$i]=1
	
	for((j=1;j<i;j++))
	do
		a=${prev_line[$((j-1))]}
		b=${prev_line[$j]}
		current_line[$j]=$((a+b))
	done
	
	prev_line=("${current_line[@]}") 
	echo ${current_line[@]}
done

