from multiprocessing import Process, Event, Manager
from time import sleep
from App.Helpers import *
class BaseParallel:
    """
    ### Explanation:
    This Base Parallel class is class make any class run in parallel 
    """
    def set_parallel(self, cls, clsattr:str, args, logger:dict, categoryName:str, name:str) -> None:
        """
        ### Explanation:
        This method prepare the attribute needed for parallel concept
        ### Args:
        @cls: class, the class you want to execute in parallel, required.
        @clsattr: string, name of the method want to execute in interval way, required.
        @args: list, arguments that will be passed into the class init method, required.
        ### return:
        None
        """
        self.parallel_shared_state = Manager().dict()
        self.parallel_process:Process|None = None
        self.parallel_cls = cls
        self.parallel_clsattr = clsattr
        self.parallel_cls_args = args
        self.parallel_pauseEv = Event() 
        self.parallel_stopEv = Event()
        self.parallel_issuccess_stopEv = Event()
        self.parallel_logger = logger
        self.parallel_cat_name = categoryName
        self.name = name

    def start_parallel(self, cls, clsattr:str, args:list, logger:dict, categoryName:str, name:str) -> bool:
        """
        ### Explanation:
        This method is entry point to start class in parallel, "it will be instantiated inside the parallel process". 
        ### Args:
        @cls: class, the class you want to execute in parallel, required.
        @clsattr: string, name of the method want to execute in interval way, required.
        @args: list, arguments that will be passed into the class init method, required.
        ### return:
        bool: True if started else false.
        """
        started = False
        if not hasattr(self, "parallel_process"): self.parallel_process = None
        if self.parallel_process == None:    
            started = True
            self.set_parallel(cls, clsattr, args, logger, categoryName, name)
            self.parallel_process = Process(target=self.parallel, args=(self.parallel_cls, self.parallel_clsattr, self.parallel_pauseEv, self.parallel_stopEv, self.parallel_logger, self.parallel_cat_name, self.name, self.parallel_shared_state, *self.parallel_cls_args))    
            self.parallel_process.start()
        return started

    def stop_parallel(self, timeout:float = None) -> None:
        """
        ### Explanation:
        This method stops the running parallel object
        ### Args:
        accept no args.
        ### return:
        None
        """
        if self.parallel_process != None:
            self.parallel_stopEv.set()
            tryJoin = False if timeout != None else True
            if timeout != None:
                reachedTimeout = milli(timeout)
                while True:
                    if self.parallel_issuccess_stopEv.is_set():
                        tryJoin = True
                        break
                    elif reachedTimeout <= milli():
                        self.parallel_process.terminate()
                        break
            
            if tryJoin: self.parallel_process.join()
            del self.parallel_process
            self.parallel_process = None

    def pause_parallel(self) -> None:
        """
        ### Explanation:
        This method pause the running parallel object
        ### Args:
        accept no args.
        ### return:
        None
        """
        if hasattr(self, "parallel_pauseEv"):
            self.parallel_pauseEv.set()

    def play_parallel(self):
        """
        ### Explanation:
        This method play the paused parallel object
        ### Args:

        ### return:

        """
        if hasattr(self, "parallel_pauseEv"):
            self.parallel_pauseEv.clear()
    
    def isPause_parallel(self) -> bool:
        """
        ### Explanation:
        This method checks whether the parallel object process is running or paused.
        ### Args:
        accept no args.
        ### return:
        bool: True for paused else False
        """
        if hasattr(self, "parallel_pauseEv"):
            return self.parallel_pauseEv.is_set()
    def parallel(self, cls, clsattr:str, pauseEv, stopEv, logger, cat_name, name, Shared_state:dict , *args) -> None:
        """
        ### Explanation:
        This method is the running method in parallel, inside it will  instantiate the class and get the inteded attribute that will be running in interval way.
        ### Args:
        @cls: class, the class you want to execute in parallel, required.
        @clsattr: string, name of the method want to execute in interval way, required.
        @pauseEv: Event, it will be fired when pausing parallel.
        @stopEv: Event, it will be fired when intending to stop the parallel completly.
        @args: list, arguments that will be passed into the class init method, required.
        ### return:
        None
        """
        obj = cls(logger, cat_name, name, *args, Parallel_args = Shared_state)
        attr = getattr(obj, clsattr)
        while True:
            try:
                if stopEv.is_set(): 
                        obj.app_close()
                        self.parallel_issuccess_stopEv.set()
                        break

                if not pauseEv.is_set():
                    attr()
                    sleep(0.01)
            except BaseException as err: 
                logE(getLogging(logger["name"], logger["path"]),f"Process of {cat_name} '{name}' catched an error", traceback.format_exc(), err)
        
    def parallel_status(self) -> str|None:
        res = None
        if self.parallel_process != None:
            if "status" in self.parallel_shared_state:
                res = self.parallel_shared_state.get("status")
        return res
    
    def parallel_ginfo(self) -> dict|None:
        res = None
        if self.parallel_process != None:
            if "ginfo" in self.parallel_shared_state:
                res = self.parallel_shared_state.get("ginfo")
        return res
        