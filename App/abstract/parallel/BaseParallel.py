from multiprocessing import Process, Event
from time import sleep

class BaseParallel:
    def set_parallel(self, cls, clsattr:str, *args) -> None:
        self.parallel_process:Process|None = None
        self.parallel_cls = cls
        self.parallel_clsattr = clsattr
        self.parallel_cls_args = args
        self.parallel_pauseEv = Event() 
        self.parallel_stopEv = Event()

    def start_parallel(self, cls, clsattr:str, *args) -> bool:
        started = False
        if not hasattr(self, "parallel_process"): self.parallel_process = None
        if self.parallel_process == None:    
            started = True
            self.set_parallel(cls, clsattr, *args)
            self.parallel_process = Process(target=self.parallel, args=(self.parallel_cls, self.parallel_clsattr, self.parallel_pauseEv, self.parallel_stopEv, *self.parallel_cls_args))    
            self.parallel_process.start()
        return started

    def stop_parallel(self):
        if self.parallel_process != None:
            self.parallel_stopEv.set()
            self.parallel_process.join()
            del self.parallel_process
            self.parallel_process = None

    def pause_parallel(self):
        if hasattr(self, "parallel_pauseEv"):
            self.parallel_pauseEv.set()

    def play_parallel(self):
        if hasattr(self, "parallel_pauseEv"):
            self.parallel_pauseEv.clear()
    
    def isPause_parallel(self):
        if hasattr(self, "parallel_pauseEv"):
            return self.parallel_pauseEv.is_set()

    def parallel(self, cls, clsattr:str, pauseEv, stopEv, *args):
        obj = cls(*args)
        attr = getattr(obj, clsattr)
        while True:
            try:
                if not pauseEv.is_set():
                    attr()
                    if stopEv.is_set(): 
                        break
                    sleep(0.01)
            except: 
                pass