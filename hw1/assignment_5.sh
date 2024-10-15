#!/bin/bash

for ((i=0;i<$1;i++))
do
	current_line=()
	for ((j=0;j<$1;j++))
	do
		if [[ $i == $j ]]; then
			current_line+="1 " 
		else
			current_line+="0 "
		fi
	done

	echo "${current_line[@]}"	
 
done 

