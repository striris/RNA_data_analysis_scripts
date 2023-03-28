from Bio.PDB import PDBParser, PDBIO
import sys

# python .\chain_and_atoms_info.py "pdb_10.pdb" "pdb_10_generated.pdb"

# Define the PDB files to compare
file1 = sys.argv[1]
file2 = sys.argv[2]

# Get names
file1_name = file1.split('/')[-1]
file2_name = file2.split('/')[-1]
print('###################################################################')
print('Comparing native: '+file1_name+', generated: '+file2_name)

# Create a PDB parser object
parser = PDBParser(QUIET=True)

# Parse both PDB files
structure1 = parser.get_structure(str(file1_name), file1)
structure2 = parser.get_structure(str(file2_name), file2)

# Count the number of chains and atoms in each chain

for structure in [structure1, structure2]:
    print(structure.get_id())
    chain_count = 0
    for chain in structure.get_chains():
        atom_count = 0
        chain_count += 1
        for residue in chain:
            for atom in residue:
                if(atom.element!='H'):
                    atom_count+=1
        print("Chain {}: {} atoms".format(chain.get_id(), atom_count))
    print("Total chains: {} \n".format(chain_count))


# Loop over the chains in both structures
for chain1, chain2 in zip(structure1.get_chains(), structure2.get_chains()):
    # Loop over the residues in both chains
    for res1, res2 in zip(chain1.get_residues(), chain2.get_residues()):
        # Check if the residues are the same
        if res1.resname != res2.resname or res1.id != res2.id:
            print('ERROR 1')

struc1_total = 0
struc2_total = 0

# Loop over the chains in both structures
for chain1, chain2 in zip(structure1.get_chains(), structure2.get_chains()):
    # Loop over the residues in both chains
    '''
    chain_total_C = 0
    chain_total_O = 0
    chain_total_N = 0
    chain_total_P = 0
    '''
    chain1_total = 0
    chain2_total = 0
    for res1, res2 in zip(chain1.get_residues(), chain2.get_residues()):
        # Check if the residues are the same
        if res1.resname == res2.resname and res1.id == res2.id:
            # Get the atoms in both residues
            atoms1 = res1.get_atoms()
            atoms2 = res2.get_atoms()
            
            # For natives structures
            C_count_native = 0
            O_count_native = 0
            N_count_native = 0
            P_count_native = 0
            X_count_native = 0

            #print('native, atoms in a residue')
            # Count the different atoms in each residue
            for atom in atoms1:

                if (atom.element != 'H'):
                    #print(atom.element)
                    #print(atom.name)
                    chain1_total+=1
                    if (atom.element == 'C'):
                        C_count_native += 1
                    elif (atom.element == 'O'):
                        O_count_native += 1
                    elif (atom.element == 'N'):
                        N_count_native += 1
                    elif (atom.element == 'P'):
                        P_count_native += 1
                    elif (atom.element == 'X'):
                        X_count_native += 1
            
            # For generated structures
            C_count_generated = 0
            O_count_generated = 0
            N_count_generated = 0
            P_count_generated = 0
            X_count_generated = 0
            
            #print('generated, atoms in a residue')
            # Count the different atoms in each residue
            for atom in atoms2:
                if (atom.element != 'H'):
                    #print(atom.element)
                    #print(atom.name)
                    chain2_total+=1
                    if (atom.element == 'C'):
                        C_count_generated += 1
                    elif (atom.element == 'O'):
                        O_count_generated += 1
                    elif (atom.element == 'N'):
                        N_count_generated += 1
                    elif (atom.element == 'P'):
                        P_count_generated += 1
                    elif (atom.element == 'X'):
                        X_count_generated += 1
            
            # Compare native and generated atoms in each residue
            if(C_count_native!=C_count_generated):
                print(f"Chain: {chain1.id}, Residue number: {res1.id[1]}, Name: {res1.resname}")
                print("Atom 'C' native: "+str(C_count_native)+', generated: '+str(C_count_generated))
                print('')
            if(O_count_native!=O_count_generated):
                print(f"Chain: {chain1.id}, Residue number: {res1.id[1]}, Name: {res1.resname}")
                print("Atom 'O' native: "+str(O_count_native)+', generated: '+str(O_count_generated))
                print('')
            if(N_count_native!=N_count_generated):
                print(f"Chain: {chain1.id}, Residue number: {res1.id[1]}, Name: {res1.resname}")
                print("Atom 'N' native: "+str(N_count_native)+', generated: '+str(N_count_generated))
                print('')
            if(P_count_native!=P_count_generated):
                print(f"Chain: {chain1.id}, Residue number: {res1.id[1]}, Name: {res1.resname}")
                print("Atom 'P' native: "+str(P_count_native)+', generated: '+str(P_count_generated))
                print('')
            if(X_count_native!=X_count_generated):
                print(f"Chain: {chain1.id}, Residue number: {res1.id[1]}, Name: {res1.resname}")
                print("Atom 'X' native: "+str(X_count_native)+', generated: '+str(X_count_generated))
                print('')

    print("chain1_total: " + str(chain1_total))
    struc1_total += chain1_total

    print("chain2_total: " + str(chain2_total))
    struc2_total += chain2_total
    print('')
        
print("struc1_total: " + str(struc1_total))
print("struc2_total: " + str(struc2_total))
print("")