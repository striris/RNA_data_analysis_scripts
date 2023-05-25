#!/bin/bash

# Assign a value to a variable
declare -a list=("1A4D" "1CSL" "1DQF" "1MHK")

# Loop through a sequence of numbers using the variable
for i in ${list[@]}; 
do
	echo ${i} >> unique_chains_results.txt
	(time rna_denovo.cxx11thread.linuxgccrelease @${i}_flags) 2>> unique_chains_results.txt
done

#rna_denovo.cxx11thread.linuxgccrelease @flags
