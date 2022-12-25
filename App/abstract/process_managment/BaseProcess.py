from abc import ABC, abstractmethod
from App.Helpers import *
import datetime
class BaseProcess(ABC):
    """
    ### Explanation:
    This abstract class is used with each process want to integrate it in BaseMultiProcessing
    ### Args:
    @args: list, arguments that will be needed by the process, required.
    ### return:
    None
    """
    def __init__(self, logger:dict, cat_name:str, name:str, *args, Parallel_args:dict = None) -> None:
        self.logger = logger
        self.categoryName = cat_name
        self.name = name
        self.__parallel_args = Parallel_args
        self.status = ""
        self.initilize(*args)
        
    @property
    def events(self)-> list[str]:
        """
        which events the process is listening to, this typehint is added forcebly so don't try to check it with hasattr().
        """
        return []

    @abstractmethod
    def initilize(self, *args) -> None:
        """
        ### Explanation:
        This method is executed when class is created don't try to fetch data from other processes that inherit process_management abstract concept.
        ### Args:
        @args: list, argument needed by the process, required.
        ### return:
        None
        """
        pass

    @abstractmethod
    def run(self, event:str) -> None:
        """
        ### Explanation:
        this method meant to execute the process in interval way.
        ### Args:
        @event: string [ any event inside the listeners of events/listeners], this sepcify which event been executed and called the service, required.
        ### return:
        None
        ### Note:
        the @event arg it will be ommitted when running in parallel so be sure to remove it when running the process in parallel. 
        """
        pass
    
    @abstractmethod
    def app_close(self):
        """
        ### Explanation:
        abstarct magic method executed when removing the class object from mem.
        ### Args:
        accept no args.
        ### return:
        None
        """
        pass
    
    def log_success(self, Title:str, *args, Epath:str = None):
        logS(getLogging(self.logger["name"], self.logger["path"]), Title, *args, Epath = Epath )
    
    def debugMsg(self, message:str, *args, Force:bool = False, specificFile:str =None) -> None:
        """
        ### Explanation:
        This function used to print your message into console if the app is running in debug mode.
        ### Args:
        @message: can be String, is used to hold the message you want to log, required.  
        @Force: can be bool, used to force debug, default: False.
        @specificFile: can be String {"name":"name to register in memory", "path":"temp/logs/FileName.log", "rotation":"1 MB"}, used to set specific file to write the debug message helpful with parallel, default: None.
        @args: can be dataType, is a list param that will be formatted inside the @message string, default: empty list.
        ### return: 
        None
        ### Examples: 
        from App.Helpers import *\n
        debugMsg("Hello {}!", "World")
        """
        debugMsg(message, *args, Force=Force, specificFile={"name":self.logger['name'], "path":self.logger['path']})

    def exec_command(self, cmName:str, action:str, metaData:dict = {}, type:str = "normal" ) -> Any|None:
        if hasattr(self, "parallel"):
            return exec_command(cmName, action, metaData, type)
        else:
            app = getApplication(True)
            if app == None: return None
            app.commands.exec_command(cmName, action, metaData)
    
    def set_status(self, stats:str):
        if isinstance(stats, str):
            stats = stats + "|" + str(datetime.datetime.now())
            if hasattr(self, "parallel"):
                self.__parallel_args["status"] = stats
            else:
                self.status = stats
    
    def stop(self):
        self.exec_command(f"{self.categoryName}Commands", f"stop_{self.categoryName}", {f"{self.categoryName}_name":self.name, "timeout":1})