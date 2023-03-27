import __main__
import glob
import os
#import pandas as pd
import pymol
import time


def align(mobile, reference):
    """Do a sequence alignment between two pdbs and write the output.
    Parameters
    ----------
    mobile : A PDB file. Sequence will be first in the alignment.
    reference : A PDB file. Sequence will be second in alignment.
    filename : Output name of alignment file.
    """
    __main__.pymol_argv = ['pymol', '-qc']
    pymol.finish_launching()
    pymol.cmd.load(mobile)
    pymol.cmd.load(reference)
    obj = list(pymol.cmd.get_object_list('all'))
    print(pymol.cmd.align(obj[0], obj[1], cycles=0,transform=1))
    pymol.cmd.reinitialize()
    time.sleep(1)

puzzle_number_list = [1,  2,  3,  4,  5,  6,  7,   9, 10, 11, 12, 13, '14b', '14f', 15, 17, 18, 19, 20, 21]
pdbID_list = ['3MEI','3P59','3OWZ','3V7E','4P9R','4GXY','4R4V','5KPY','4LCK','5LYV','4QLM','4XW7','5DDP','5DDO','5DI4','5K7C','5TPY','5T5A','5Y87','5NWQ']

orig_sys = sys.stdout
with open('output.txt','w') as out:
    sys.stdout = out
    for i in range(20):
        align('./pdb'+str(pdbID_list[i]).lower()+'.ent', '../puzzle_21_ares_natives/pdb_'+str(puzzle_number_list[i])+'.pdb')
        #pymol.cmd.load('../puzzle_21_ares_natives/pdb_'+str(puzzle_number_list[i])+'.pdb')
        #print(puzzle_number_list[i])



 
