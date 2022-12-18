from App.Helpers import *
from App.abstract.process_managment.BaseProcess import BaseProcess
from App.abstract.process_managment.BaseMultiProcess import BaseMultiProcess
from abc import ABC, abstractmethod
class BaseProcesses(ABC):
    """
    ### Explanation:
    this class meant to be the processes manager for each process
    ### Args :
    accept no args.
    """
    def __init__(self) -> None:
        self.app = getApplication(True)
        if not self.app: raise Exception(f"No Application has been detected in {__file__}")
        self.processes : list[BaseMultiProcess] = []
        self.initilize() 

    @property
    @abstractmethod
    def processname(self) -> str:
        """
        this property set the name of the intended process
        """
        pass

    @property
    @abstractmethod
    def processespath(self) -> str:
        """
        this property set the path of processes to load
        """
        pass

    @property
    @abstractmethod
    def processesManagerPath(self) -> str:
        """
        this property set the path of process manager class which extends BaseMultiProcess
        """
        pass

    def initilize(self) -> None:
        """
        ### Explanation:
        This method get executed when app is registered in processes manager and also processes bag is created
        ### Args:
        accept no args.
        ### return:
        None
        """
        debugMsg(f"Loading {self.processname}s ...")
        ProcessesfilePath = self.processespath
        ProcessManager = getattr(importlib.import_module(self.processesManagerPath.replace("/", ".")), self.processname)
        if not issubclass(ProcessManager, BaseMultiProcess): raise ApplicationCatchedError(f"{self.processname} Manager isn't subclass of BaseMultiProcess")
        filesNames = [ f.replace(".py", "") for f in os.listdir(ProcessesfilePath) if not re.match('__.*__', f)]
        idCounter = 0
        for n in filesNames:
            idCounter+=1
            filePath = (ProcessesfilePath.replace("/",".") + (("." + n)))
            m = importlib.import_module(filePath)
            cls = getattr(m, n)
            if issubclass(cls, BaseProcess):
                self.add_process(ProcessManager(idCounter, n, cls, filePath, True, self.app))
                debugMsg(f"loaded {self.processname}"" : {}", filePath)
    
    def run_processes(self, event) -> None:
        """
        ### Explanation:
        This is the entry point for every event launched by events class which run specific event for specific process listeners
        ### Args:
        @event: string [ any event inside the listeners of events/listeners], this sepcify which event been executed and called the process, required.
        ### return:
        None
        """
        processes = self.get_processes()
        for s in processes:
            s.run(event)

    def add_process(self, processObj) -> None:
        """
        ### Explanation:
        this method add process to the processes bag
        ### Args:
        @processObj: object, the single process managing class, required. 
        """
        self.processes.append(processObj)
    
    def get_processes(self) -> list[BaseMultiProcess]:
        """
        ### Explanation:
        this method return all of the process managing classes
        ### Args:
        accept no args.
        ### return:
        list, containing the process managing object.
        """
        return self.processes
    
    def get_process(self, name:str) -> BaseMultiProcess|None:
        """
        ### Explanation:
        this method return the process managing class according to the provided name.
        ### Args:
        @name: string, name of the wanted process to retreive, required.
        ### return:
        object, containing the process managing object.
        None, if the process not found.
        """
        S = None
        for s in self.processes:
            if s.name == name:
                S = s

        return S