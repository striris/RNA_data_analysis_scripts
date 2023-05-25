#!/bin/bash

# Assign a value to a variable
declare -a list=("1ESY" "1KKA" "1L2X" "1Q9A" "1QWA" "1XJR" "255D" "283D" "28SP" "2A43" "2F88")

# Loop through a sequence of numbers using the variable
for i in ${list[@]}; 
do
	echo ${i} >> single_chain_results.txt
	(time rna_denovo.cxx11thread.linuxgccrelease @${i}_flags) 2>> single_chain_results.txt

done

#rna_denovo.cxx11thread.linuxgccrelease @flags
