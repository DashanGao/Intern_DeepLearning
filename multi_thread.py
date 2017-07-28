import threading


class MultiThreadWrap(threading.Thread):
    def __init__(self, num_thread, work_list, mutex_func, work_func):
        threading.Thread.__init__(self)
        self.mutex_func = mutex_func
        self.work_list = work_list
        self.work_func = work_func
        self.num_thread = num_thread

    def run(self):
        while self.work_list:
            lock.acquire()
            i = self.work_list.pop()
            lock.release()
            self.work_func(i)

            lock.acquire()
            self.mutex_func(i)
            lock.release()

    def start(self):
        for i in range(num_thread):
            threading.Thread.start(self)

