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

        ##For specific process
        if metaData.get(f"{self.processname}_name","undefined") == "undefined": raise Exception(f"{self.processname} Name undefiend")
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
            timeout = metaData.get("timeout", False)
            if timeout:
                p.stop(timeout)
            else:
                p.stop()
                
            self.returnCMres(True, True)

        elif action == f"get_status_{self.processname}":
            p = self.get_specific_procs(metaData)
            response = p.status()
            if response != None:
                self.returnCMres(True, response)
            else:
                self.returnCMres(False, f"""{self.processname}_{metaData[f"{self.processname}_name"]}_closed""")

    def get_specific_procs(self, metaData:dict) -> BaseMultiProcess:
        p = self.process.get(metaData[f"{self.processname}_name"])
        if p == None: raise Exception(f"{self.processname} name is not registered in our {self.processname} manager")
        return p
    
    