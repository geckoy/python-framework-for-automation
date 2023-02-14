from App.Helpers import *
from abc import ABC
from App.abstract.process_managment.BaseProcess import BaseProcess
from App.abstract.parallel.BaseParallel import BaseParallel
class BaseMultiProcess(ABC, BaseParallel):
    """
    ### Explanation:
    This class is Process managing class which stop pause start the process of the BaseProcesses
    ### Args:
    @id: int, process identification, required.
    @name:string, name of the process, required.
    @cls:class, the real process class, required.
    @path: string, path of the real process class in form of MainFolder.SubFolder.FileName, required.
    @autoStart:bool, if auto launch at starting, required.
    @categoryName: string, name of this category of process for example service, required. 
    @args: list, argument that will be passed to the real process class at instantiation, default: empty list.
    ### return:
    None
    """
    def __init__(self, *, id:int, name:str, cls:BaseProcess, path:str, autoStart:bool, categoryName:str, args:list = []) -> None:
        self.id = id
        self.name = name
        self.process_class = cls
        self.process_path = path
        self.categoryName = categoryName
        self.autoStart = autoStart
        self.loggingName = f"{self.name}"
        self.loggerPath = f"temp/logs/processes/{self.categoryName}/{self.loggingName}.log"
        self.logger = {"name":self.loggingName, "path":self.loggerPath}
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
        if not self.isParallel:
            if self.autoStart:
                self.start()

    def run(self, event:str) -> None:
        """
        ### Explanation:
        this method meant to execute the process in interval way, works only for sync mode.
        ### Args:
        @event: string [ any event inside the listeners of events/listeners], this sepcify which event been executed and called the process, required.
        ### return:
        None
        """
        if  not self.isParallel:
            if hasattr(self.process_obj, "virtual") and event == "app_loop_process":
                self.__run()
                
            elif self.process_obj != None and hasattr(self.process_obj, "events"):
                if event in self.process_obj.events:
                    self.__run(event)
        else:
            if not hasattr(self, "called_parallel"):
                setattr(self, "called_parallel", True)
                if self.autoStart:
                    self.start()
                
    def __run(self, event:str = None):
        if not self.isPaused(): 
            try:
                if event != None : 
                    self.process_obj.run(event)
                else:
                    self.process_obj.run()
            except KeyboardInterrupt as err:
                raise err
            except BaseException as err:
                logE(getLogging(self.loggingName, self.loggerPath),f"Process of {self.categoryName} '{self.name}' catched an error", traceback.format_exc(), err)

    def start(self) -> bool:
        """
        ### Explanation:
        start the process, real class will be instantiated.
        ### Args:
        accept no args.
        ### return:
        bool, True if started else False
        """
        started = False
        if self.isParallel:
            started = self.start_parallel(self.process_class, "run", self.process_args, {"name":self.loggingName, "path":self.loggerPath}, self.categoryName, self.name)
        elif self.process_obj == None: 
            started = True
            self.process_obj = self.process_class(self.logger, self.categoryName, self.name, *self.process_args)

        return started

    def stop(self, timeout:float =None):
        """
        ### Explanation:
        destroy the process memory allocation "destruct the object"
        ### Args:
        @timeout: float, define the timeout for parallel to terminate it instead of waiting till process end, default: None.
        ### return:
        None
        """
        if self.isParallel:
            self.stop_parallel(timeout)

        elif not self.process_obj == None:
            self.process_obj.app_close()
            del self.process_obj
            self.process_obj = None
    
    def isInstantiated(self) -> bool:
        """return whether the process object is instantiated or not

        ## Returns:
            ``bool``: true is process is instantiated else false.
        """
        if self.isParallel:
            return True if self.parallel_process else False
        else:
            return True if self.process_obj else False
    
    def isPaused(self) -> bool:
        """
        ### Explanation:
        return whether the process is paused or running
        ### Args:
        accept no args
        ### return:
        bool, True for paused else False
        """
        if self.isParallel:
            return self.isPause_parallel()
        else:
            return self.paused

    def pause(self) -> None:
        """
        ### Explanation:
        this method pause the running process.
        ### Args:
        accept no args.
        ### return:
        None
        """
        if self.isParallel:
            self.pause_parallel()
        else:
            self.paused = True
    
    def unPause(self) -> None:
        """
        ### Explanation:
        this method play the paused process.
        ### Args:
        accept no args.
        ### return:
        None
        """
        if self.isParallel:
            self.play_parallel()
        else:
            self.paused = False
    
    def app_close(self):
        """
        ### Explanation:
        this method called by events.py when app is closing, which inside it will call the stop method to stop the running process.
        ### Args:
        accept no args.
        ### return:
        None
        """
        self.stop(0.1)
    
    def status(self) -> None|str:
        """
        None, when process is closed
        str, response from process
        """
        res = None
        if self.isParallel:
            res = self.parallel_status()
        else:
            if self.process_obj != None:
                res = self.process_obj.status
        
        return res
    
    def ginfo(self) -> None|dict:
        """
        None, when process is closed
        dict, response from process
        """
        res = None
        if self.isParallel:
            res = self.parallel_ginfo() 
            res = res if res != None else {}
            res = {**res, "status":self.parallel_status() } 
        else:
            if self.process_obj != None:
                res = {**self.process_obj.ginfo, "status": self.process_obj.status}
            else:
                res = {"status":None}
        BaseInfo = {
            "isPaused":self.isPaused(),
            "isInstantiated":self.isInstantiated()
        }
        if res:
            res = {**res, **BaseInfo}
        else:
            res = BaseInfo

        return res