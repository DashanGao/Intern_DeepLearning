import threading


class MultiThreadWrap():
    def __init__(self, num_thread, work_list, mutex_func, work_func):
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
            while self.work_list:
                self.lock.acquire()
                i = self.work_list.pop()
                self.lock.release()
                self.work_func(i)

                self.lock.acquire()
                self.mutex_func(i)
                self.lock.release()

    def start(self):
        lock = threading.Lock()
        thread_pool = []
        for i in range(self.num_thread):
            th = self.jThread(self.num_thread, self.work_list, self.mutex_func, self.work_func, lock)
            th.start()
            thread_pool.append(th)
        for i in thread_pool:
            i.join()

