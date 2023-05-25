import json
number = 1
with open('fasta_and_secstruc.txt') as file:
    print('start')
    for line in file.readlines():
        line = line.replace('\n', '')
        if number == 1:
            ID = line[1:5]
            print(ID)
            new_file = open(str(ID)+"_c.fasta", "w")
            new_file.write(line.lower())
            new_file.write('\n')
            new_file.close()
        if number == 2:
            new_file = open(str(ID)+"_c.fasta", "a")
            new_file.write(line)
            new_file.close()
        if number == 3:
            new_file = open(str(ID)+".secstruc", "w")
            new_file.write(line)
            new_file.close()
            number = 0
        
        number = number +1