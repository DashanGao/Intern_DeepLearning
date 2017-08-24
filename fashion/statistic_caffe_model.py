# -*- coding: utf-8 -*-

import sys
import os
import val
import time
import cPickle
import datetime
import logging
import flask
import werkzeug
import optparse
import numpy as np
import pandas as pd
from PIL import Image
import cStringIO as StringIO
import urllib
import exifutil
import fashion_demo_exe as classifyer
import caffe
import cv2

os.environ["CUDA_VISIBLE_DEVICES"] = "4"
CLASS_LIST = "/home/dasgao/download/pva-faster-rcnn/data/logo258/class_list_Chinese.txt"
root = '/home/dasgao/download/pva-faster-rcnn/'
val_list = root + "data/logo258/val_list.txt"
deploy = root + 'models/pvanet/example_train/logo258_test.prototxt'
caffe_model = root + 'output/faster_rcnn_pvanet/logo258_train/pvanet_frcnn_iter_100000.caffemodel'
img_mean = root + 'caffe-fast-rcnn/python/caffe/imagenet/ilsvrc_2012_mean.npy'
img_dir = root + 'data/logo258/dataset/imgs/'
out_file = "result.txt"

clf = classifyer.ImageClassifyer()
clf.net.forward()

# _classes = []
# with open(CLASS_LIST) as f:
#     for l in f:
#         _classes.append(l.strip().split(" ")[1].encode(encoding='UTF-8', errors='strict'))
# _classes = tuple(_classes)
# _ind_to_class = dict(zip(xrange(len(_classes)), _classes))


def clfy(filename):
    result = clf.classify(filename)
    out_cls = [x[0] for x in result]
    out_bbox = [x[1:5] for x in result]
    confidence = np.array([x[5] for x in result], dtype=np.float)
    sorted_ind = np.argsort(-confidence)
    confidence = [confidence[x] for x in sorted_ind]
    out_cls = [out_cls[x] for x in sorted_ind]
    out_bbox = np.array([out_bbox[x] for x in sorted_ind], dtype=np.int32)
    ret = []
    for i in range(len(out_cls)):
        if out_cls[i] != 0:
            ret.append([out_cls[i]] + out_bbox[i].tolist() + [confidence[i]])
    return ret

if __name__ == '__main__':
    num = int(sys.argv[1])
    with open(val_list, "r") as val:
        vals = val.readlines()
    for i in range(num):
        val = img_dir + vals[i].strip()
    if not os.path.isfile(val):
        print val,"wrong"
        exit()
        ret = clfy(val)
        with open(out_file, "a") as out:
            out.write(str(ret)+"\n")
