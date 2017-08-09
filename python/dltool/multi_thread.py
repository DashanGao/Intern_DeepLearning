import threading


class MultiThreadWrap():
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
        self.mutex_func = mutex_func
        self.work_list = work_list
        self.work_func = work_func
        self.num_thread = num_thread

    class jThread(threading.Thread):
        def __init__(self, num_thread, work_list, mutex_func, work_func, lock):
            threading.Thread.__init__(self)
            self.mutex_func = mutex_func
            self.work_list = work_list
            self.work_func = work_func
            self.num_thread = num_thread
            self.lock = lock

        def run(self):
            while True:

                self.lock.acquire()
                if len(self.work_list) == 0:
                    self.lock.release()
                    break
                i = self.work_list.pop()
                self.lock.release()

                self.work_func(i)

                self.lock.acquire()
                self.mutex_func(i)
                self.lock.release()

    def start(self):
        """
        call it to start asynchromous multi thread with block
        :return: return None after all threads have exit
        """
        lock = threading.Lock()
        thread_pool = []
        for i in range(self.num_thread):
            th = self.jThread(self.num_thread, self.work_list, self.mutex_func, self.work_func, lock)
            th.start()
            thread_pool.append(th)
        for i in thread_pool:
            i.join()

