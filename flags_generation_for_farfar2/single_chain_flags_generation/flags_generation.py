import os
import json
# generate flags file for farfar2 execution for single structure
# execute in flags folder
for ID in ["1ESY","1KKA","1L2X","1Q9A","1QWA","1XJR","255D","283D","28SP","2A43","2F88"]:
    print(ID)
    flag_file = open(ID+"_flags", "w")
    flag_file.write("-fasta ../extraction/single_chain/"+ID+"_1.fasta\n")
    flag_file.write("-native ../pdb_files/"+ID+".pdb\n")
    flag_file.write("-secstruct_file ../extraction/single_chain/"+ID+"_1.secstruct\n")
    flag_file.write("-nstruct 1000\n")
    flag_file.write("-out:file:silent ../../output_files/"+ID+".out\n")
    flag_file.write("-cycles 1000\n")
    flag_file.write("-minimize_rna\n")

    flag_file.close()