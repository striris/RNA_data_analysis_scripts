#!/bin/bash

# Assign a value to a variable
declare -a list=("157D" "1I9X" "1KD5")

# Loop through a sequence of numbers using the variable
for i in ${list[@]}; 
do
	echo ${i} >> dup_chains_results.txt
	(time rna_denovo.cxx11thread.linuxgccrelease @${i}_flags) 2>> dup_chains_results.txt
done

#rna_denovo.cxx11thread.linuxgccrelease @flags
