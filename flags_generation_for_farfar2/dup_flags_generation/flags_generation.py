import os
import json
# generate flags file for farfar2 execution for single structure
# execute in flags folder
for ID in ["157D","1I9X","1KD5"]:
    print(ID)
    flag_file = open(ID+"_flags", "w")
    flag_file.write("-fasta ../extraction/dup_chains/split/"+ID+"_c.fasta\n") #_c means comma separated 
    flag_file.write("-native ../pdb_files/"+ID+".pdb\n")
    flag_file.write("-secstruct_file ../extraction/dup_chains/split/"+ID+".secstruct\n")
    flag_file.write("-nstruct 1000\n")
    flag_file.write("-out:file:silent ../../output_files/"+ID+".out\n")
    flag_file.write("-cycles 1000\n")
    flag_file.write("-minimize_rna\n")

    flag_file.close()