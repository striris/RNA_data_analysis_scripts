import os

folder = r'./'
count = 1

ID_list = [1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, '14b', '14f', 15, 17, 18, 19, 20, 21]
# count increase by 1 in each iteration
# iterate all files from a directory
for file_name in os.listdir(folder):
    # Construct old file name
    source = folder + file_name
    if (os.path.splitext(file_name)[-1]=='pdb'):
        # Get name of the file
        only_name = os.path.splitext(file_name)[0]
        print(only_name)
        # Construct new name
        puzzle_number = only_name.split('_')[2]
        if (puzzle_number==str(14)):
            if (only_name.split('_')[3]==('bound')):
                puzzle_number='14b'
            elif (only_name.split('_')[3]=='free'): 
                puzzle_number='14f'
        print(puzzle_number)
        # Adding the count to the new file name and extension
        destination = folder + "pdb_" + str(puzzle_number) + ".pdb"

        # Renaming the file
        os.rename(source, destination)
        count += 1

print('All Files Renamed')

print('New Names are')
# verify the result
res = os.listdir(folder)
print(res)