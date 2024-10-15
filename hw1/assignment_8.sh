#!/bin/bash

random_number=$(($RANDOM%(101)))

for((i=1;i<=10;i++))
do
	read -p "Enter a number from 0 to 100: " number

	while ! [[ $number =~ ^(100|[1-9]?[0-9])$ ]]
	do
		read -p "Incorrect input! Enter a number from 0 to 100: " number
	done

	if [[ $number -eq $random_number ]]; then
		echo "You won! Number of attempts: $i"
		exit 0
	elif [[ $number -le $random_number ]]; then
		echo "Nah! My number is greater than $number"
	else
		echo "Nah! My number is less than $number"
	fi
done

echo "You exceeded given attempts and lost the game =( The number was: $random_number"	
