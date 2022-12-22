from abc import ABC, abstractmethod
from App.Helpers import *

class BaseProcess(ABC):
    """
    ### Explanation:
    This abstract class is used with each process want to integrate it in BaseMultiProcessing
    ### Args:
    @args: list, arguments that will be needed by the process, required.
    ### return:
    None
    """
    def __init__(self, logger:dict, cat_name:str, name:str, *args) -> None:
        self.logger = logger
        self.categoryName = cat_name
        self.name = name
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

    def exec_command(self):
        pass