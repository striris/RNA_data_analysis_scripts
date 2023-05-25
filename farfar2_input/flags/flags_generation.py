import os
import json
# generate flags file for farfar2 execution for structures with unique chains
# execute in flags folder
for ID in ["1A4D","1CSL","1DQF","1MHK"]:
    print(ID)
    flag_file = open(ID+"_flags", "w")
    flag_file.write("-fasta ../extraction/unique_chains/"+ID+"_c.fasta\n") #_c means comma separated 
    flag_file.write("-native ../pdb_files/"+ID+".pdb\n")
    flag_file.write("-secstruct_file ../extraction/unique_chains/"+ID+".secstruct\n")
    flag_file.write("-nstruct 1000\n")
    flag_file.write("-out:file:silent ../../output_files/"+ID+".out\n")
    flag_file.write("-cycles 1000\n")
    flag_file.write("-minimize_rna\n")

    flag_file.close()