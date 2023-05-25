#!/bin/bash

# Assign a value to a variable
declare -a list=("1CSL" "1DQF" "1MHK")

# Loop through a sequence of numbers using the variable
for i in ${list[@]};
do
        echo ${i}
        RNAcofold < ${i}.fasta | sed -n 2p > ${i}.secstruct
done
