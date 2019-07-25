import sys
import os
import file_diff

dict1 = dict()
dict2 = dict()

folder1, folder2 = sys.argv[1], sys.argv[2]

for idict, ifolder in zip([dict1, dict2], [folder1, folder2]):
    for root, dirs, files in os.walk(ifolder):
        folder_name = root.replace(ifolder, ".")
        idict[folder_name] = dict()
        idict[folder_name]["list"] = [x for x in files if len(x) > 2 and x[-2:] == '.c']
        idict[folder_name]["set"] = set(idict[folder_name]["list"])

folder_set_1 = set(dict1.keys())
folder_set_2 = set(dict2.keys())

folder_set_1_exclusive = folder_set_1 - folder_set_2
folder_set_2_exclusive = folder_set_2 - folder_set_1

folder_set_common = folder_set_1.intersection(folder_set_2)

files_dir_1_exclusive = []
files_dir_2_exclusive = []

changes_in_files = []

for folder_name in folder_set_common:
    A = dict1[folder_name]["set"] - dict2[folder_name]["set"]
    B = dict2[folder_name]["set"] - dict1[folder_name]["set"]
    files_dir_1_exclusive.extend([folder_name + "/" + x for x in A])
    files_dir_2_exclusive.extend([folder_name + "/" + x for x in B])
    C = dict1[folder_name]["set"].intersection(dict2[folder_name]["set"])
    for ic in C:
        file1 = folder1 + folder_name[1:] + "/" + ic
        file2 = folder2 + folder_name[1:] + "/" + ic
        print(file1, file2)
        changes = file_diff.get_diff_files(file1 , file2)
        if changes is not None:
            changes_in_files.append(changes)


print(folder_set_1_exclusive)
print(folder_set_2_exclusive)
print(files_dir_1_exclusive)
print(files_dir_2_exclusive)
print(changes_in_files)

