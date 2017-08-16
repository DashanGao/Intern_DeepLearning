import json
import glob


def extract_inst(dic):
    res = {}
    labels = []
    count = 0
    for img in dic.iterkeys():
        if len(dic[img][u"category"]) > 1 :
            continue
        if len(dic[img][u"category"]) == 0:
            # print dic[img]
            continue
        count += 1
        label = dic[img][u"label"]
        labels.append(label)
        cate = dic[img][u"category"][0]

        if not res.has_key(label):
            res[label] = {u"category": cate, u"img": [{u"path": img, u"boxes_detected": dic[img][u"doxes_detexted"][0]}]}
        else:
            if res[label][u"category"] == cate:
                res[label][u"img"].append({u"path": img, u"boxes_detected": dic[img][u"doxes_detexted"][0]})
    labels = list(set(labels))
    for lb in labels:
        if len(res[lb][u"img"]) < 5:
            del res[lb]
    print count, "imgs"
    return res


def extract_inst_file(file_):
    with open(file_, "r") as dt:
        dic = json.load(dt)
    return extract_inst(dic)


def count_multi_cate(src):
    tmp = 0
    with open(src, "r") as sr:
        data = json.load(sr)
    for i in data.itervalues():
        if len(i["category"]) != 1:
            tmp += 1
    print tmp, len(data)


if __name__ == '__main__':
    # f = sys.argv[1]
    # if len(sys.argv) == 3:
    #     prefix = sys.argv[2]
    # else:
    #     print "wrong"
    #     exit()
    fs = glob.glob("fdata/*")
    for f in fs:
        print f
        processed_dic = extract_inst_file(f)
        with open(f.replace("fdata/", "processed_data/pro"), "w") as des:
            json.dump(processed_dic, des)

