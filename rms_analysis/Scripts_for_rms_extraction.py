import os
import sys

array_rms = []
pdbID = sys.argv[1]
print(pdbID)
path = '../out_pdb_'+pdbID
entries = os.scandir(path) # change it to your directory that stores pdb files
# for values store in one folder
for entry in entries:
    ext = os.path.splitext(entry)[-1].lower()
    if ext==".pdb":
        with open(entry) as file:
            for line in file.readlines():
                line = line.replace('\n', '')
                if ('rms' in line) and ('stem' not in line):
                    file_full_name = os.path.basename(entry)
                    file_name = os.path.splitext(file_full_name)[0]
                    new_file = open(pdbID+"_pdb_rms.txt", "a")
                    rms = line[4:]
                    array_rms.append(rms)
                    new_file.write(file_name + ':' + str(rms) + '\n')

                    new_file.close()
