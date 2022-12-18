from multiprocessing import Process
from abc import ABC
class BaseMultiProcess(ABC):
    """
    ### Explanation:
    This class is Process managing class which stop pause start the processes 'service also can use this class'
    ### Args:
    @id: int, process identification, required.
    @name:string, name of the process, required.
    @cls:class, the real process class, required.
    @path: string, path of the real process class, required.
    @autoStart:bool, if auto launch at starting, required.
    @args: list, argument that will be passed to the real process class at instantiation, default: empty list.
    ### return:
    None
    """
    def __init__(self, id:int, name:str, cls, path:str, autoStart:bool, *args) -> None:
        self.id = id
        self.name = name
        self.process_class = cls
        self.process_path = path
        self.autoStart = autoStart
        self.process_args = args
        self.process_obj = None
        self.isPreviouslyStop = False
        self.isParallel = True if hasattr(cls, "parallel") else False
        self.initilize()

    def initilize(self) -> None:
        """
        ### Explanation:
        executed after the process manager has registered everything.
        ### Args:
        accept no args
        ### return:
        None
        """
        self.paused = self.unPause()
        if self.autoStart:
            self.start()

    def run(self, event) -> None:
        """
        ### Explanation:
        this method meant to execute the process in interval way.
        ### Args:
        @event: string [ any event inside the listeners of events/listeners], this sepcify which event been executed and called the process, required.
        ### return:
        None
        """
        if self.process_obj != None and not self.isParallel and hasattr(self.process_obj, "events"):
            if event in self.process_obj.events:
                if not self.isPaused(): self.process_obj.run(event)
    
    def start(self) -> bool:
        """
        ### Explanation:
        init the process
        ### Args:
        accept no args.
        ### return:
        bool, True if started else False
        """
        started = False
        if self.process_obj == None and not self.isPreviouslyStop: 
            started = True
            if self.isParallel:
                pass
            else:
                self.process_obj = self.process_class(*self.process_args)
        return started

    def stop(self):
        """
        ### Explanation:
        destroy the process memory allocation "destruct the object"
        ### Args:
        accept no args.
        ### return:
        None
        """
        if not self.process_obj == None:
            self.isPreviouslyStop = True
            if self.isParallel:
                pass
            else:
                del self.process_obj
                self.process_obj = None
    
    def isPaused(self):
        if self.isParallel:
            pass
        else:
            return self.paused

    def pause(self):
        if self.isParallel:
            pass
        else:
            self.paused = True
    
    def unPause(self):
        if self.isParallel:
            pass
        else:
            self.paused = False
    
    def parallel(self):
        pass
    
    def __del__(self):
        if self.process_obj != None: 
            self.stop()