from App.Helpers import *
from abc import ABC
from App.abstract.process_managment.BaseProcess import BaseProcess
from App.abstract.parallel.BaseParallel import BaseParallel
class BaseMultiProcess(ABC, BaseParallel):
    """
    ### Explanation:
    This class is Process managing class which stop pause start the processes 'service also can use this class'
    ### Args:
    @id: int, process identification, required.
    @name:string, name of the process, required.
    @cls:class, the real process class, required.
    @path: string, path of the real process class in form of MainFolder.SubFolder.FileName, required.
    @autoStart:bool, if auto launch at starting, required.
    @categoryName: string, name of this category for example service, required. 
    @args: list, argument that will be passed to the real process class at instantiation, default: empty list.
    ### return:
    None
    """
    def __init__(self, id:int, name:str, cls, path:str, autoStart:bool, categoryName:str, *args) -> None:
        self.id = id
        self.name = name
        self.process_class = cls
        self.process_path = path
        self.categoryName = categoryName
        self.autoStart = autoStart
        self.logger = getLogging(f"{self.name}_{self.id}", f"temp/logs/processes/{self.categoryName}/{self.name}.log")
        self.process_args = args
        self.process_obj :BaseProcess|None = None
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

    def run(self, event:str) -> None:
        """
        ### Explanation:
        this method meant to execute the process in interval way.
        ### Args:
        @event: string [ any event inside the listeners of events/listeners], this sepcify which event been executed and called the process, required.
        ### return:
        None
        """
        if  not self.isParallel:
            if self.process_obj != None and hasattr(self.process_obj, "events"):
                if event in self.process_obj.events:
                    self.__run(event)
    
    def __run(self, event:str = ""):
        if not self.isPaused(): 
            self.process_obj.run(event)

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
        if self.isParallel:
            started = self.start_parallel(self.process_class, "run")
        elif self.process_obj == None: 
            started = True
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
        if self.isParallel:
            self.stop_parallel()

        elif not self.process_obj == None:
            self.process_obj.app_close()
            del self.process_obj
            self.process_obj = None
    
    def isPaused(self):
        if self.isParallel:
            self.isPause_parallel()
        else:
            return self.paused

    def pause(self):
        if self.isParallel:
            self.pause_parallel()
        else:
            self.paused = True
    
    def unPause(self):
        if self.isParallel:
            self.play_parallel()
        else:
            self.paused = False
    
    def app_close(self):
        self.stop()