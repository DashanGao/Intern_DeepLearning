import glob
import time
from util import parse_json as pjson
import os
import json
import numpy as np

class DetectorVal:
    def __init__(self, snapshot_format="val_snapshot"):

        snap_list = glob.glob(snapshot_format + "*")
        self.snapshot_file = snapshot_format + "_" + time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime()) + ".txt"
        if snap_list:
            # need recover?
            print("Temp file found: recover? ignore?")
            print("0 - Ignore")
            for idx, item in enumerate(snap_list):
                print(str(idx + 1) + " - " + item)
            select = int(raw_input("Which? Input : "))
            if select != 0:
                self.snapshot_file = snap_list[select - 1]
        if os.path.isfile(self.snapshot_file):
            with open(self.snapshot_file, 'r') as f:
                record = [json.loads(x) for x in f]
                self.img_file = [x['item'] for x in record]
        else:
            self.img_file = []
        self.fd = open(self.snapshot_file, 'a')

    def need_exe(self, img_file):
        return img_file not in self.img_file

    def record(self, img_file, gt_cls, gt_bbox, cls, bbox, score):
        new_record = {}
        new_record['item'] = img_file
        confidence = np.array([x for x in score], dtype=np.float)
        sorted_ind = np.argsort(-confidence)
        cls = [cls[x] for x in sorted_ind]
        bbox = [bbox[x] for x in sorted_ind]
        score = [score[x] for x in sorted_ind]
        new_record['out'] = [{'cls': cls[i], 'bbox': bbox[i], 'score': score[i]} for i in range(len(score))]
        new_record['gt'] = [{'cls': gt_cls[i], 'bbox': gt_bbox[i]} for i in range(len(gt_cls))]
        self.fd.write(json.dumps(new_record) + "\n")
        self.fd.flush()

    def summary(self, confidence_threshold, bbox_threshold=0.7, delete=True, extra=False):
        self.fd.close()
        with open(self.snapshot_file) as f:
            records = [json.loads(x) for x in f]

        for i in xrange(len(records)):
            gt = records[i]['gt']
            out = records[i]['out']
            for j in range(len(gt)):
                gt[j]['result_cls'] = -1
                gt[j]['result_bbox'] = -1

            gt_bbox = np.array([x['bbox'] for x in gt], dtype=np.float)
            out_bbox = np.array([x['bbox'] for x in out], dtype=np.float)
            out_score = np.array([x['score'] for x in out], dtype=np.float)

            for idx in range(len(gt)):
                xmin = np.maximum(gt_bbox[idx, 0], out_bbox[:, 0])
                ymin = np.maximum(gt_bbox[idx, 1], out_bbox[:, 1])
                xmax = np.minimum(gt_bbox[idx, 2], out_bbox[:, 2])
                ymax = np.minimum(gt_bbox[idx, 3], out_bbox[:, 3])
                w = np.maximum(xmax - xmin + 1., 0.)
                h = np.maximum(ymax - ymin + 1., 0.)
                inters = w * h
                uni = ((gt_bbox[idx, 2] - gt_bbox[idx, 0] + 1.) * (gt_bbox[idx, 3] - gt_bbox[idx, 1] + 1.) +
                       (out_bbox[:, 2] - out_bbox[:, 0] + 1.) * (out_bbox[:, 3] - out_bbox[:, 1] + 1.) - inters)
                overlap = inters / uni
                ovmax = np.max(overlap)
                jmax = np.argmax(overlap)

                if ovmax > bbox_threshold:
                    gt[idx]['result_bbox'] = True
                    if out_score[jmax] > confidence_threshold:
                        if out[jmax]['cls'] == gt[idx]['cls']:
                            gt[idx]['result_cls'] = True
                        else:
                            gt[idx]['result_cls'] = out[jmax]['cls']

        results = {}
        for i in records:
            for j in i['gt']:
                if j['cls'] not in results.keys():
                    results[j['cls']] = {'results': []}

        for i in records:
            for j in i['gt']:
                results[j['cls']]['results'].append({'item': i['item'],
                                         'result_cls': j['result_cls'],
                                         'result_bbox': j['result_cls']})

        ignore_list = []
        for i in results:
            cls_result = results[i]['results']
            if len(cls_result) == 0:
                print("Warning class " + str(i) + " don't have any relevant samples")
                ignore_list.append(i)
                continue
            results[i]['relevant'] = len(cls_result)
            tp = 0
            for j in cls_result:
                if j['result_bbox'] is True and j['result_cls'] is True:
                    tp += 1
            results[i]['tp'] = tp
            selected = 0
            for j in records:
                for k in j['out']:
                    if k['cls'] == i:
                        selected += 1
            results[i]['selected'] = selected
            results[i]['recall'] = float(tp) / float(results[i]['relevant'])
            results[i]['precision'] = float(tp) / float(selected) if selected != 0 else 0.

        m_recall = 0.
        m_precision = 0.
        for i in results:
            if i not in ignore_list:
                m_recall += results[i]['recall']
                m_precision += results[i]['precision']
        m_recall = m_recall / (len(results.keys()) - len(ignore_list))
        m_precision = m_precision / (len(results.keys()) - len(ignore_list))

        ret = {}
        for i in results:
            if i not in ignore_list:
                ret[i] = {}
                ret[i]['recall'] = results[i]['recall']
                ret[i]['precision'] = results[i]['precision']
        ret['mean'] = {}
        ret['mean']['recall'] = m_recall
        ret['mean']['precision'] = m_precision

        if delete:
            os.remove(self.snapshot_file)
        if extra:
            return results, ret
        return ret
