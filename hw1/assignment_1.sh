#!/bin/bash

num1=$1
num2=$2

if ! [[ "$num1" =~ ^-?[0-9]+$ && "$num2" =~ ^-?[0-9]+$ ]]; then
	echo "ERROR: please enter numbers"
	exit 1
fi

sum=$((num1 + num2))

echo "The sum is $sum" 
