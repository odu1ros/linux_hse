#!/bin/bash

typeset -A options_array

# a named array with game options associated with numbers
options_array["paper"]=0
options_array["scissors"]=1
options_array["rock"]=2

# the same but inversed
options_array_inverse=("paper" "scissors" "rock")

# a function that randomly chooses computer's response
# return: number [0-2]
# example use: get_computer_choise
get_computer_choise () {
	echo $(($RANDOM%3))
}

# associate user input with a number from options_array
# pass 1: user input
# pass 2: options_array
# return: a number associated with game optio (if string input and options_array are passed)
# or a string association with a number (if number input and options_array_inverse input)
# example use: process_user_input 1 options_array_inverse (returns "scissors")
process_user_input () {
	local user_input=$1
	shift
	local -n array=$1
 
	echo "${array[$user_input]}"
}

# a function that gets the result of a round
# pass 1: user input
# pass 2: computer input
# return: round result: 1 - win, 0 - draw, -1 - loss
# example use: get_round_result 0 1 (returns -1, paper vs scissors is loss)
get_round_result () {
	# get info of user - computer
	local result=$(($1 - $2))
 
	# user wins if result is 1 or -2, draw is 0, other options are a loss (-1 and 2)
	if [[ $result -eq 1 || $result -eq -2 ]]; then
		echo "1" 
	elif [[ $result -eq 0 ]]; then
		echo "0" 
	else
		echo "-1"
	fi
}

# we want user to specify the number of rounds he wishes to play
read -p "Specify the number of rounds you wish to play: " number_rounds
while ! [[ $number_rounds =~ ^[1-9][0-9]*$ ]]; do
	read -p "Incorrect input! Please, enter a positive integer: " number_rounds
done

score_comp=0
score_user=0

# go for rounds
while true
do
	# get a random number from a computer and associate it with optional game words
	comp_choise=$(get_computer_choise)
	comp_choise_word=$(process_user_input "$comp_choise" options_array_inverse)
 
	# get input from user in a correct form
	read -p "Please, enter one of the options: rock, scissors, paper: " user_inp

	while ! [[ "$user_inp" == "paper" || "$user_inp" == "scissors" || "$user_inp" == "rock" ]]; do
		read -p "Please, enter one of the options: rock, scissors, paper: " user_inp
	done
 
	# associate user input with a number
	user_choise=$(process_user_input "$user_inp" options_array)
 
	# get result
	round_result=$(get_round_result "$user_choise" "$comp_choise")
 
	# print out result, update scores
	if [[ $round_result -eq 1 ]]; then
		score_user=$((score_user+1))
		echo "Opponent's choise was $comp_choise_word . You won the round! Current score is $score_user - $score_comp"
	elif [[ $round_result -eq 0 ]]; then
		echo "Opponent's choise was $comp_choise_word . A draw! Current score is $score_user - $score_comp"
	else
		score_comp=$((score_comp+1))
		echo "Opponent's choise was $comp_choise_word . You lost the round! Current score is $score_user - $score_comp"
	fi
 
	# game finishes when either computer or user gets enough points
	if [[ $score_comp -eq $number_rounds ]]; then
		echo "You lost the game within $number_rounds rounds =("
		break
	elif [[ $score_user -eq $number_rounds ]]; then
		echo "You won the game within $number_rounds rounds =)"
		break
	fi
done
