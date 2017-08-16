import os
import json
import glob
import time


def mkdir_imgs(fi):
    st = time.clock()
    with open(fi, "r") as da:
        data = json.load(da)
    for instance in data.iterkeys():
        cate = data[instance]["category"]
        cate_path = os.path.join(des_path, cate)
        instance_path = os.path.join(cate_path, instance)

        if not os.path.exists(cate_path):
            os.mkdir(cate_path)
        if not os.path.exists(instance_path):
            os.mkdir(instance_path)
        for img in data[instance]["img"]:
            img = img["path"]
            src_file = os.path.join(src_path, img)
            target_file = os.path.join(instance_path, img.split("/")[-1])
            if not os.path.isfile(target_file):
                open(target_file, "wb").write(open(src_file, "rb").read())
        print fi, "finished", (time.clock()-st), "seconds used"


if __name__ == '__main__':
    src_path = "/opt/data-safe/users/terrencege"
    des_path = "/opt/data-safe/users/dasgao/CCCV_img"
    fis = glob.glob("pro*.json")
    for fi_ in fis:
        mkdir_imgs(fi_)

