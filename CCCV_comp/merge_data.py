import json
import sys
import os

# dic1 = {"1": "1,2", "2": "12,34,1", "ds": "1,5,6"}
# dic2 = {"1": "3, 5, 6", "2": "1, 6, 7, 8"}
# dic1.update(dic2)
# print dic1
# exit()
'''
command line run: 
merge a into b
python merge_json a.json b.json
'''


def three_file_merge(file_1, file_2, file_3):
    with open(file_1, "r") as patch:
        tmp = json.load(patch)
    with open(file_2, "r") as src:
        data = json.load(src)

    data.update(tmp)
    with open(file_3, "w") as clct:
        json.dump(data, clct)


def two_file_merge(data_patch, collector):
    with open(data_patch, "r") as patch:
        tmp = json.load(patch)
    if os.path.isfile(collector):
        with open(collector, "r") as src:
            data = json.load(src)
    else:
        data = {}
    data.update(tmp)
    with open(collector, "w") as clct:
        json.dump(data, clct)


if __name__ == '__main__':
    if len(sys.argv) == 3:
        two_file_merge(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 4:
        three_file_merge(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print '''
command line run: 
merge a into b
python merge_json a.json b.json
'''
