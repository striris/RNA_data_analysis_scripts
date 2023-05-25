#!/bin/bash

# Assign a value to a variable
declare -a list=("1" "2" "3" "4" "5" "6" "7" "8" "9" "10" "11" "12" "13" "14f" "14b" "15" "17" "18" "19" "20" "21")
# Loop through a sequence of numbers using the variable
mkdir out_fasta
for i in ${list[@]};
do
	python pdb2fasta.py ../rna_puzzle_${i}.pdb > ./out_fasta/out_fasta_${i}.fasta
done
