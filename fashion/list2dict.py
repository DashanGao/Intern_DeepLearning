from balanc import get_train_val
import os


dic = {}
for i in range(1, 3):
    dic[str(i)] = []
for i in range(4, 11):
    dic[str(i)] = []

with open('list_test.txt', 'r') as li:
    lis = li.readlines()
    for li_ in lis:
        li_.strip()
        with open(os.path.join('gts', li_.replace(r'jpg', 'txt').strip()), "r") as img:
            features = img.readlines()
            print features[0].strip()
            for feature in features:
                cate = feature.split(' ')[4].strip()
                dic[str(int(cate)+1)].append(li_.strip())
for key in dic.iterkeys():
    print key, len(dic[key])
# print dic
# :q
# get_train_val(dic, 0.1)
