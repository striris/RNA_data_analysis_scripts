#!/bin/bash

# Assign a value to a variable
declare -a list=("1" "2" "3" "4" "5" "6" "7" "8" "9" "10" "11" "12" "13" "14f" "14b" "15" "17" "18" "19" "20" "21")
# Loop through a sequence of numbers using the variable
for i in ${list[@]};
do
	cat out_fasta_${i}.fasta >> ares_near_native_fasta.txt
done
