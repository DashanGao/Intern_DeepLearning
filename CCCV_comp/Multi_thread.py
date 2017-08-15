import threading
import time
import Queue
import os
import email_notifier as em
from multiprocessing import cpu_count
import json
import subprocess

'Config ----------------------------------------------'
src_file = "pailitao_train_list_108w_to_end.txt"
db_name = "CCCV_pailitao_img_query_108w_to_end.json"
thread_num = cpu_count() * 2

# thread_num = 1

'-----------------------------------------------------'

exit_flag = 0


class Processor(threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID

    def run(self):
        while not exit_flag:
            process(self.threadID)


def process(threadID):
    # 1. Pop data
    queue_lock.acquire()
    line1 = record_queue.get()
    line2 = record_queue.get()
    line3 = record_queue.get()
    line4 = record_queue.get()

    q_size = record_queue.qsize()
    queue_lock.release()
    if q_size % 100 == 0:
        print q_size

    # # 2. Check if record exists
    # img1 = line1.strip().split()[0]
    # img2 = line2.strip().split()[0]
    # img3 = line3.strip().split()[0]
    # img4 = line4.strip().split()[0]
    #
    # file_lock.acquire()
    # with open(db_name, 'r') as outfile:
    #     try:
    #         js = json.load(outfile)
    #     except:
    #         print outfile.read()
    #         print "!!!!!!\n\n\n\n"
    #     if js.has_key(img1):
    #         file_lock.release()
    #         outfile.close()
    #         print "Img exists"
    #         return
    # file_lock.release()

    # 3. Process data
    port = threadID % 4
    if port == 3:
        port = 8080
    else:
        port = port + 8083
    dic1 = query(line1, str(port))
    dic2 = query(line2, str(port))
    dic3 = query(line3, str(port))
    dic4 = query(line4, str(port))


    # 4. Write into file
    file_lock.acquire()
    with open(db_name, 'r') as outfile_:
        try:
            js = json.load(outfile_)
        except:
            js = {}
    js.update(dic1)
    js.update(dic2)
    js.update(dic3)
    js.update(dic4)

    with open(db_name, 'w') as writ:
        json.dump(js, writ)
    file_lock.release()


def query(line, port):
    res = line.strip().split()
    label = res[1]
    img = res[0]
    print img, '      img___'
    cmd = "curl -X POST -F \"search=@/opt/data-safe/users/terrencege/" + img + "\" 10.20.3.12:"+port+"/service/detect/cloth"
    # cmd = "curl -X POST -F \"search=@/home/gaodashan/Pictures/" + img + "\" 10.20.3.12:8080/service/detect/cloth"

    s = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    result = json.loads(s.communicate()[0])["boxes_detected"]
    cates = [i[u"type"] for i in result]
    dic = {"category": cates, "doxes_detexted": result, "label": label}
    print dic
    return {img: dic}


if __name__ == '__main__':
    # lock for page queue
    queue_lock = threading.Lock()
    file_lock = threading.Lock()
    record_queue = Queue.Queue()
    threads = []  # thread pool

    # Init outfile
    if not os.path.isfile(db_name):
        with open(db_name, 'w') as outfil:
            outfil.write("{}")
        outfil.close()
        print "CREATED"

    # Init queue
    queue_lock.acquire()
    with open(src_file, 'r') as src:
        lines = src.readlines()
        for i in range(0, len(lines)):
            st = lines[i].replace("/opt/data/users/yuhang/data/", "")
            record_queue.put(st)
    queue_lock.release()

    # Start threads
    print 'Feature number: ', record_queue.qsize()
    print 'Start processing...'
    threadID = 1
    for threadNum in range(thread_num):
        thread = Processor(threadID)
        thread.start()
        threads.append(thread)
        threadID += 1

    # Wait for finish.
    while not record_queue.empty():
        pass
    exit_flag = 1
    em.send("Local img query finish", "108W to end")
    for t in threads:
        t.join()

    print 'Finish'

