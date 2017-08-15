import re_ranking_Jianku
import threading
import time
import Queue
import os
from multiprocessing import cpu_count
import json

'Config ----------------------------------------------'
# Set the src npy file as "feature.npy"

start = 110000
stop = 220000

thread_num = cpu_count()*2
db_name = "R_star_db"+str(start)+".json"
'-----------------------------------------------------'

exit_flag = 0


class Processor(threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID

    def run(self):
        while not exit_flag:
            process()


def process():
    # 1. Pop data
    queue_lock.acquire()
    img = record_queue.get()
    q_size = record_queue.qsize()
    queue_lock.release()
    if q_size % 10 == 0:
        print q_size, "left"

    # 2. Check if record exists
    file_lock.acquire()
    with open(db_name, 'r') as outfile:
        try:
            js = json.load(outfile)
        except:
            print outfile.read()
            print "!!!!!!\n\n\n\n"
        if js.has_key(img):
            outfile.close()
            return
    file_lock.release()

    # 3. Process data
    # Do something here
    r_star = re_ranking_Jianku.reciprocal_star(img)
    dic = {str(img): r_star}
    print dic

    # 4. Write into file
    file_lock.acquire()
    with open(db_name, 'r') as outfile_:
        try:
            js = json.load(outfile_)
        except:
            js = {}
    js.update(dic)
    with open(db_name, 'w') as writ:
        json.dump(js, writ)
    file_lock.release()


if __name__ == '__main__':
    # # record initial time
    # start_time = time.clock()
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
    for i in range(start, stop):
        record_queue.put(i)
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
    for t in threads:
        t.join()

    print 'Finish'

