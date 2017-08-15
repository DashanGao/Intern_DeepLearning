import numpy as np

'''
By Dashan Gao 
@ 2917.8.10

This script reads a txt file, convert every line in this file to a np.array and endure it into a npy file. 
Save data every 1000 records to save memory, accelerate the process. 
This script can be modified easily to adapt new file format.
'''

source_file = "feat_final.txt"
dest_file = "feature_final.npy"
FE = None
FN = None
flag = 0
with open(source_file, "r") as feat:
    fes = feat.readlines()
    for i in range(len(fes)):
        if i % 1000 == 999:
            if flag == 0:
                np.save(dest_file, FE)
                flag = 1
            else:
                FN = np.load(dest_file)
                FN = np.vstack((FN, FE))
                np.save(dest_file, FN)
            FE = None
            print i
        if FE is None:
            FE = np.array(map(eval, fes[0].strip().split()[1:]))
        else:
            FE = np.vstack((FE, map(eval, fes[0].strip().split()[1:])))
if FE is not None:
    FN = np.load(dest_file)
    FN = np.vstack((FN, FE))
    np.save(dest_file, FN)
