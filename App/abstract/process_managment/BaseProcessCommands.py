from App.Helpers import *
from abc import ABC, abstractmethod
from App.abstract.process_managment.BaseProcesses import BaseProcesses
from App.abstract.process_managment.BaseMultiProcess import BaseMultiProcess

class BaseProcessCommands(ABC):

    @property
    @abstractmethod
    def processname(self) -> str:
        pass

    def execAbstract(self, action:str, metaData:dict) -> exec_command_returned_dict:
        self.process :BaseProcesses = getattr(self.app, self.processname)
        if action == f"start_{self.processname}":
            p = self.get_specific_procs(metaData)
            r = p.start()
            self.returnCMres(r, r)
        elif action == f"pause_{self.processname}":
            p = self.get_specific_procs(metaData)
            p.pause()
            self.returnCMres(True, True)
        elif action == f"unpause_{self.processname}":
            p = self.get_specific_procs(metaData)
            p.unPause()
            self.returnCMres(True, True)
        elif action == f"stop_{self.processname}":
            p = self.get_specific_procs(metaData)
            p.stop()
            self.returnCMres(True, True)
    
    def get_specific_procs(self, metaData:dict) -> BaseMultiProcess:
        if metaData.get(f"{self.processname}_name","undefined") == "undefined": raise Exception(f"{self.processname} Name undefiend")
        p = self.process.get(metaData[f"{self.processname}_name"])
        if p == None: raise Exception(f"{self.processname} name is not registered in our {self.processname} manager")
        return p
    
    