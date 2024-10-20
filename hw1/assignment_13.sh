#!/bin/bash

words_file="ohio_plants_hangman.txt"
# shuffle and select first word
word=$(shuf -n 1 "$words_file")

# an array of underscores
masked_word=""
for ((i=0; i<${#word}; i++)); do 
	masked_word+="_"
done

# current errors count, max errors label, incorrect letters array
errors=0
max_errors=6
incorrect_letters=()

# printing out current game state: guessed letters, incorrect letters, asking for a new input
function echo_game_state {
	echo "$masked_word"
	echo "Errors ($errors): ${incorrect_letters[*]}"
	echo -n "Input a letter: "
}

# update masked word if the guessed letter is correct
# pass 1: guessed letter
# returns nothing, only updates global masked_word
function update_masked_word {
	local input_letter=$1
	local new_masked_word=""
  
	for ((i=0; i<${#word}; i++)); do
		if [[ ${word:$i:1} == "$input_letter" ]]; then
			new_masked_word+="$input_letter"
		else
			new_masked_word+="${masked_word:$i:1}"
		fi
	done

	masked_word=$new_masked_word
}

# until the word is guessed or errors number < 6 play a game
while [[ "${masked_word[*]}" != "$word" && $errors -lt $max_errors ]]; do
	echo_game_state
	read -n1 input
	echo

	# check if user input is correct:
	# 1) it should be a letter a-z any case
	# 2) the letter should not be guessed already (either be anywhere within masked_word or incorrect_letters)
	while [[ ! "$input" =~ [a-zA-Z] || "${masked_word}" == *"$input"* || "${incorrect_letters[*]}" == *"$input"* ]]; do
		read -n1 -p "Input a letter: " input
		echo
	done
  	
  	# convert input to lowercase if needed
	input=$(echo "$input" | tr '[:upper:]' '[:lower:]')
  
	# now try finding input inside word:
	# 1) if it is present, update the mask
	# 2) if it is not, count+ errors and add it to incorrect letters array
	if [[ "$word" == *"$input"* ]]; then
		update_masked_word "$input"
	else
		incorrect_letters+=("$input")
		((errors++))
	fi
done

# now the result
if [[ "$masked_word" == "$word" ]]; then
	echo "Congratulations! You guessed the word: $word"
else
	echo "Game over! The correct word was: $word"
fi
