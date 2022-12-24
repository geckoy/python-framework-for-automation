from App.Helpers import *
from abc import ABC, abstractmethod
from App.abstract.process_managment.BaseProcess import BaseProcess
from App.abstract.process_managment.BaseMultiProcess import BaseMultiProcess
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
        setattr(self.app, self.processname, self)
        debugMsg("{} Data: {}", self.processname,str([ f"name: {s.name}, isParallel: {s.isParallel}" for s in self.get_all()]).replace("['","\n ").replace("']","").replace("',","\n").replace("'",""))

    @property
    @abstractmethod
    def processname(self) -> str:
        """
        this property set the category name of the intended process, keep in mind the process manager that extends from BaseMultiprocess class should have this name 'manager for single process'
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
        this property set the path of process manager class which extends BaseMultiProcess 'manager single process'
        """
        pass

    def initilize(self) -> None:
        """
        ### Explanation:
        This method get executed when all needed attribute are registered.
        ### Args:
        accept no args.
        ### return:
        None
        ### Note:
        FilePath variable should be in format of MainFolder.SubFolder. ...etc .FILE
        """
        ProcessesToregister:list[dict] = []
        debugMsg(f"Loading {self.processname}s ...")
        ProcessesfilePath = self.processespath
        ProcessManager = getattr(importlib.import_module(self.processesManagerPath.replace("/", ".")), self.processname)
        if not issubclass(ProcessManager, BaseMultiProcess): raise ApplicationCatchedError(f"{self.processname} Manager isn't subclass of BaseMultiProcess")
        
        if not hasattr(self, "virtual"):
            filesNames = [ f.replace(".py", "") for f in os.listdir(ProcessesfilePath) if not re.match('__.*__', f)]
            idCounter = 0
            for n in filesNames:
                idCounter+=1
                filePath = (ProcessesfilePath.replace("/",".") + (("." + n)))
                m = importlib.import_module(filePath)
                cls = getattr(m, n)
                if issubclass(cls, BaseProcess):
                    ProcessesToregister.append({
                        "id":idCounter, 
                        "name":n, 
                        "cls":cls, 
                        "path":filePath, 
                        "autoStart":True, 
                        "categoryName":self.processname, 
                        "args":[]
                    })
        else:
            if not hasattr(self, "get_vdata"): raise Exception(f"Abstract BaseProcesses can't find method get_vdata in process {self.processname}")
            self.get_vdata()
            vdatas = self.set_vdata(retreive=True)
            
            for d in vdatas:
                m = importlib.import_module(d["path"] + "." + self.processname)
                cls = getattr(m, self.processname)
                cls.virtual = True
                if issubclass(cls, BaseProcess):
                    d["cls"] = cls 
                    ProcessesToregister.append(d)


        for P in ProcessesToregister:
            if issubclass(P["cls"], BaseProcess):
                self.add_process(ProcessManager(**P))
                if not hasattr(self, "virtual"): 
                    debugMsg(f"loaded {self.processname}"" : {}", P["path"])
                else:
                    debugMsg("loaded {} : {}", self.processname, P["name"])

    def run(self, event) -> None:
        """
        ### Explanation:
        This is the entry point for every event launched by events class which run specific process for specific event, virtual get executed only with app_loop_process event.
        ### Args:
        @event: string [ any event inside the listeners of events/listeners], this sepcify which event been executed and called the process, required.
        ### return:
        None
        """
        if event == "app_loop_process":
            if not hasattr(self, "virtual"):
                return
        else:
            if hasattr(self, "virtual"):
                return

        processes = self.get_all()
        for s in processes:
            s.run(event)

    def add_process(self, processObj:BaseMultiProcess) -> None:
        """
        ### Explanation:
        this method add process that extends BaseMultiProcess to the processes bag
        ### Args:
        @processObj: object, the single process managing class extends BaseMultiProcess, required. 
        ### return:
        None.
        """
        self.processes.append(processObj)
    
    def get_all(self) -> list[BaseMultiProcess]:
        """
        ### Explanation:
        this method return all of the process managing classes that extends BaseMultiProcess
        ### Args:
        accept no args.
        ### return:
        list, containing the process managing object that extends BaseMultiProcess.
        """
        return self.processes
    
    def get(self, name:str) -> BaseMultiProcess|None:
        """
        ### Explanation:
        this method return the process managing class that extends BaseMultiProcess according to the provided name.
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

    def set_vdata(self, id:int = None, name:str = None, autoStart:bool = None, args:list = [], *, retreive = False, __stored:list = []) -> list[dict]|None:
        """
        ### Explanation:
        This method add the data needed for virtual BaseProcesses to create BaseMultiProcess Manager class, each time you call it will be added to the static list.
        ### Args:
        @id: int, the identification you want to give for the process manager that extends BaseMultiProcess, required.
        @name: string, name that you want to provide for process manager class that extrends BaseMultiProcess, required.
        @autoStart: bool, whether to start auto the process or not, required.
        @args: list, arguments that need to be passed to the real process class, default: empty array.
        ### return:
        None, when registering data.
        list, when trying to retreive the registered datas. 
        """
        if (id == None or name == None or autoStart == None) and retreive == False:raise Exception(f"Please fille all the vdata in process {self.processname}") 
        if not retreive:
            __stored.append({
                "id":id, 
                "name":name, 
                "autoStart":autoStart, 
                "args":args,
                "path":self.processespath.replace("/","."),
                "categoryName":self.processname
            })
        else:
            st = __stored.copy()
            __stored.clear()
            return st

    @classmethod
    def inheritors_classes(klass) -> list:
        """
        This method return the classes that inherit the BaseProcesses class.
        """
        for d in listdir():
            if re.match(".*Process", d, re.IGNORECASE):
                processname = d.replace("Process", "")
                path = f"{processname}Process.general.{processname}Manager"
                importlib.import_module(path)
        subclasses = []
        work = [klass]
        while work:
            parent = work.pop()
            for child in parent.__subclasses__():
                if child not in subclasses:
                    subclasses.append(child)
                    work.append(child)
        return subclasses
    
    @classmethod
    def inheritors(klass) -> list:
        """
        This method return the object that inherit the BaseProcesses class based on their process name will be retreived from the application.
        """
        inherits = []
        app = getApplication(True)
        if app == None: raise Exception("No app is found")
        PROCESSES : list[BaseProcesses] = klass.inheritors_classes()
        for P in PROCESSES:
            try:
                if not isDebug():
                    if P.processname == "psample" or P.processname == "vpsample":
                        continue
                inherits.append(getattr(app, P.processname))
            except:
                applogE("BaseProcess inheritors can't find process prop in app of process ", P.processname)
        return inherits
