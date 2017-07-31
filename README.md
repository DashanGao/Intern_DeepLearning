# dltool
File List
=============
| File   | Use     |
| -------|:------|
|util.py | general usage |
|figure.py | draw      |
|val.py | detector test tool|
|multi_thread.py| multi thread wrapper|
|balance.py|balance train val data|
Function
=============
balance.py
-----------------
#####get_train_val
```Python
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
```
multi_thread.py
---------------------
#####class MultiThreadWrap()

```Python
"""
asynchronized blocked multi thread with mutex lock wrapper, you can use it for download
1. set a work list
2. pop one item as i from list
3. call work_func(i)
4. call mutex_func(i)
5. go to (2) until work_list is empty
6. return None
"""
def __init__(self, num_thread, work_list, mutex_func, work_func):
    """
    :param num_thread: thread number
    :param work_list: also param list, pop 1 item from work list and pass it to mutex_func and work_func
    :param mutex_func: do something must be serial, typically write log file
    :param work_func: parallel work function
    """
def start(self):
    """
    call it to start asynchromous multi thread with block
    :return: return None after all threads have exit
    """
```
e.g. see example/multi_thread.py.example
val.py
----------
######class DetectorVal()
```Python
    def __init__(self, snapshot_format="val_snapshot"):
        """
        :param snapshot_format: temp file prefix, followed by time
        """
    def need_exe(self, img_file):
        """
        check if need to execute this test case
        :param img_file: test case id
        :return: if need to execute
        """
    def record(self, img_file, gt_cls, gt_bbox, cls, bbox, score):
        """
        add one record to snapshot file
        :param img_file: image id
        :param gt_cls: image ground truth class name, a list for multi target
        :param gt_bbox: image ground truth bbox, a 2D list, [[top left x, top left y, bottom right x, bottom right y], ...]
        :param cls: net output class, a list
        :param bbox: net output bbox, 2D lsit
        :param score: net output confidence scores, a list
        :return: None
        """
    def summary(self, confidence_threshold, bbox_threshold=0.5, delete=True, extra=False):
        """
        Retrieval summary
        :param confidence_threshold: only consider confidence > confidence_threshold results
        :param bbox_threshold: only consider bbox overlap > bbox_threshold results
        :param delete: if delete temp file after summary
        :param extra: if need extra return info
        :return: a diction which keys are class name and 1 extra 'mean' class,
                 each key has attribute 'recall' and 'precision'
                 {'cls1' : {'recall' : 0.99, 'precision' : 0.8},
                 'cls2' : {'recall' : 0.86, 'precision' : 0.65}
                 ...
                 'mean' : {'recall' : 0.901, 'precision' : 0.685}}
        """
```
Usage.   
See example/val.py.example 
```Python
dv = DetectorVal()
for item in list:
    if df.need_exe(item):
        # do something
        dv.record(...)
print(dv.summary())
```
figure.py
----------
######gird
```Python
def grid(data, saveimg, x_label=[], y_label=[], size=None, title=None):
    """
    draw a grid distribution figure(confusion matrix)
    :param data: a 2D numpy array you want to draw on figure
    :param saveimg: save image path
    :param x_label: a sequential x label string list, len(x_label) == data.shape[1](column)
    :param y_label: a sequential x label string list, len(y_label) == data.shape[0](row)
    :param size: tuple - (width, height)
    :param title: title
    :return: None
    """
```
![Eexample img](/example/confusion_matrix1.png)
![Eexample img](/example/confusion_matrix2.png)
######plot
```Python
def plot(file, x, y, xlim=None, ylim=None, name=None, align="top", save="img.png", xlabel="", ylabel="", title="", savetxt=None):
    """
    Draw plot, multi source files, multi lines, optional smooth, xlabel, ylabel, legend, title, save line data to txt
    Only need to provide txt pattern to extract data, e.g. - "Test net output #2: loss = {num}"
    :param file_x_y_drop: tuple or list of tuple - (file, x, y, drop)
                          [(file, [x1_pattern, ...], [y1_pattern, ...], [drop1, ...](optional)), ...]
                          drop1 - a int, average adjacent drop1 points to smooth line, default no smooth
    :param xlim: x axis value limitation
    :param ylim: same as xlim
    :param legend: legend name, len(x) == len(y) == len(name)
    :param align: if lenth of x/y pare in extracted number not equal, align at top or bottom
    :param xlabel: x label
    :param ylabel: y label
    :param title: image title
    :param saveimg: str, if need to save image, default not save
    :param savetxt: str. if need to save data in txt, default not save
    :return: None
    """
```
Usage.   
See example/ploy.py.example    
![Eexample img](/example/plot.png)
util.py
----------
######num_extractor
```Python
def num_extractor(lines, pattern, recall=[-1]):
    :param lines: a string
    :param pattern: pattern to match, put {num} at number you want to extract
                    multi {num} is supported, but not *, / or other special chars
    :param recall: a list marks return index
    :return: a list of extracted number
```
e.g.:   
```Python
pattern = "Iteration {num}, loss = {num}"
recall = [1]
lines = "
I0710 07:38:12.300302 35476 solver.cpp:240] Iteration 398900, loss = 0.0158956\n
I0710 07:38:12.301368 35476 solver.cpp:255]     Train net output #0: loss = 0.00447209 (* 1 = 0.00447209 loss)\n
I0710 07:38:12.301380 35476 solver.cpp:640] Iteration 398900, lr = 0.00442368\n
I0710 07:38:29.711834 35476 solver.cpp:240] Iteration 398950, loss = 0.0173632\n
I0710 07:38:29.711897 35476 solver.cpp:255]     Train net output #0: loss = 0.0222224 (* 1 = 0.0222224 loss)\n
I0710 07:38:29.711911 35476 solver.cpp:640] Iteration 398950, lr = 0.00442368\n
I0710 07:38:53.051653 35476 solver.cpp:344] Model Synchronization Communication time 0.0422409 second\n
I0710 07:38:53.051781 35476 solver.cpp:433] Iteration 399000, Testing net (#0)\n
I0710 07:38:55.725929 35476 solver.cpp:490]     Test net output #0: accuracy_top1 = 0.754062\n
I0710 07:38:55.725968 35476 solver.cpp:490]     Test net output #1: accuracy_top5 = 0.936562\n
I0710 07:38:55.725980 35476 solver.cpp:490]     Test net output #2: loss = 1.51432 (* 1 = 1.51432 loss)\n
I0710 07:38:56.075605 35476 solver.cpp:240] Iteration 399000, loss = 0.0146371\n
I0710 07:38:56.075662 35476 solver.cpp:255]     Train net output #0: loss = 0.00922734 (* 1 = 0.00922734 loss)\n
I0710 07:38:56.075686 35476 solver.cpp:640] Iteration 399000, lr = 0.00442368\n
"

return = np.array([0.0158956, 0.0173632, 0.0146371, 0.00442368])
```
***************************
#####parse_json
```Python
def parse_json(string, path):
    """
    :param string: string to parse, list or str
    :param path: dict path a/b/c
    :return: a list or item
    """
```
e.g.:   
```Python
path = "_id/$oid"
string = 
[r"{"_id":{"$oid":"595d97982782a600179b3fba"},"hit_id":"/201502/ec/kTi0ixKy2RewsnDJbEmE91k8XMynMOSY.jpg"}",
 r"{"_id":{"$oid":"59asdfasdfasdfasdfasdfff"},"hit_id":"/201502/ec/kTi0ixKasdfasferwqeyuytiewtrggfY.jpg"}"]

return = [r"595d97982782a600179b3fba", r"59asdfasdfasdfasdfasdfff"]
```
***************************
#####parse_str
```Python
def parse_str(string, pattern=" ", type="list", match_num=100000, key_idx=0):
    """
    :param string: string to parse, list
    :param pattern: split pattern
    :param type: either "list" or "dict", return a list or a diction
    :param match_num: split times
    :param key_idx: which idx is key value when type=="dict"
    :return: a list or dict
    """
```
