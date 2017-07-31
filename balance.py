import random
import numpy as np
import math


def get_train_val(cls2list, ratio, loop=0, prefix=None):
    """
    create prefix_train_list.txt and prefix_val_list.txt for balanced data.
    It doesn't work well if your data is ultra imbalance and in multi label cases.
    No overlap between val list and train list
    :param cls2list: a dict {class name : info list(whatever you want to write to the file), ...}
                            {"cls1" : ["img1.png", "img2.png", ...],
                            "cls1" : ["img1.png", "img2.png", ...], ...}
    :param ratio: 0 ~ 1, percentage of val data
    :param loop: balance loop, guarantee 100% data usage by default
    :param prefix: file prefix
    :return: None
    """
    if 0 < ratio < 1 is False:
        raise ValueError("ratio should be 0 ~ 1")
    if loop < 0:
        raise ValueError("loop should not be negative")
    ratio_init = ratio

    info_list = [x for x in cls2list.values()]
    list_len = np.array([len(x) for x in info_list], dtype=np.int32)

    info_sum = {}
    for i in info_list:
        for j in i:
            info_sum[j] = 0
    [random.shuffle(x) for x in info_list]

    # balance random select
    num_match = False
    while num_match is not True:
        val_list = []
        for i in info_list:
            val_list += i[0 : int(math.ceil(len(i) * ratio))]
        dedup_val_list = {}
        for i in val_list:
            dedup_val_list[i] = 0
        val_list = dedup_val_list.keys()
        if len(val_list) > len(info_sum) * (ratio_init + 0.02):
            ratio = ratio - 0.1 * ratio_init
        else:
            num_match = True
            print("val_list " + str(len(val_list)))
        if ratio == 0:
            print("Warning: your dataset seems too small, swith to global random select, "
                  "maybe some class will not be in val list")
    # global random select
    if num_match is not True:
        val_list = random.sample(info_sum.keys(), int(ratio_init * len(info_sum)))
        print("val_list " + str(int(ratio_init * len(info_sum))))

    # delete val info
    for i in val_list:
        info_sum[i] = -1
    for i in range(len(info_list)):
        temp = []
        for j in range(len(info_list[i])):
            if info_sum[info_list[i][j]] != -1:
                temp.append(info_list[i][j])
        info_list[i] = temp

    # sort, small to large
    list_len = np.array([len(x) for x in info_list], dtype=np.int32)
    info_list = [info_list[x] for x in np.argsort(list_len)]
    list_len = [list_len[x] for x in np.argsort(list_len)]
    print("Loop = " + str(list_len[-1]) + " will use 100% sample")
    if loop != 0:
        print("Use loop = " + str(loop))
    else:
        loop = list_len[-1]

    info_sum = {}
    for i in info_list:
        for j in i:
            info_sum[j] = 0

    train_list = []
    for i in range(loop):
        batch = []
        for j in range(len(info_list)):
            select = info_list[j][i % len(info_list[j])]
            batch.append(select)
            info_sum[select] = 1
        random.shuffle(batch)
        train_list += batch
    train_sum_num = len(info_sum.keys())
    train_use = np.sum(np.array(info_sum.values()))
    print("train list usage " + str(float(train_use) / float(train_sum_num)) +
          " (" + str(train_use) + " / " + str(train_sum_num) + ")")

    if prefix is not None:
        with open(prefix + "_val_list.txt", "w") as f:
            for i in val_list:
                f.write(i + "\n")
        with open(prefix + "_train_list.txt", "w") as f:
            for i in train_list:
                f.write(i + "\n")
    else:
        with open("val_list.txt", "w") as f:
            for i in val_list:
                f.write(i + "\n")
        with open("train_list.txt", "w") as f:
            for i in train_list:
                f.write(i + "\n")

