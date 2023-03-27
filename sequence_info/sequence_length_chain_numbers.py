import json
import os

file = open("fasta_info_list_puzzles.fasta","r")
number = 0
# generate sequence information. note down ID, number of chains, chain 1: length of sequence, chain 2: length of sequence
for line in file.readlines():
    line = line.replace('\n', '')
    if number == 1:
        new_file = open("sequence_info_puzzles_length.txt", "a")
        new_file.write(str(len(line)) + '\n')
    
    number = (number + 1)%2
new_file.close()
    