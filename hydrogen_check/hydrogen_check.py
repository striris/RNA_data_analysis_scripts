from Bio import PDB
import os

# Define a function to check for hydrogen atoms
def has_hydrogen_atoms(structure):
    for model in structure:
        for chain in model:
            for residue in chain:
                for atom in residue:
                    if atom.element == "H":
                        return True
    return False

# Define a function to check for hydrogen atoms
def hydrogen_atoms_number(structure):
    number = 0
    for model in structure:
        for chain in model:
            for residue in chain:
                for atom in residue:
                    if atom.element == "H":
                        number = number+1
    return number
    
# Load the PDB file
parser = PDB.PDBParser()
# change it to your directory that stores pdb files
entries = os.scandir(r'./') 
# for individual values in separate files
for entry in entries:
    ext = os.path.splitext(entry)[-1].lower()
    if ext==".pdb":
        file_full_name = os.path.basename(entry)
        file_name = os.path.splitext(file_full_name)[0]
        new_file = open("hydrogen_number_pdb.txt", "a")
        structure = parser.get_structure("S"+file_name, entry)
        number_hydrogen = hydrogen_atoms_number(structure)
        if  number_hydrogen > 0:
            new_file.write(file_name + " contains " + str(number_hydrogen) + " hydrogen atoms.\n")
            new_file.close()
        else:
            new_file.write(file_name+" doesn't contain any hydrogen atoms.\n")
            new_file.close()
