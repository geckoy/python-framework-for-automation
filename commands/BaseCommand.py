from abc import ABC, abstractmethod
from typing import Any
from App.Helpers import *
class BaseCommand(ABC):
    def __init__(self, name:str, filePath:str, appli) -> None:
        from app import application
        self.app :application = appli
        self.name = name
        self.filePath = filePath
        self.syncID = []
        self.__set_default_res()
        self.initilize()
        
    def execC(self, action:str, metaData:dict, uniqueID:str) -> exec_command_returned_dict:
        """
        ### Explanation:
        this method is execute specific action.
        ### Args:
        @action: string, action name to execute inside the command class, required.
        @metaData: dict, any additional data want to pass, default: empty dict.
        ### return:
        dict, return the response from executed action @status : True if all running good else False if command execution didn't occured as intended or None for exceptions or undefined action, @response for passed returned data it can be empty, e.g. { "status":True|False|None, "response":any }. 
        """
        try:
            self.__set_default_res()
            
            isSync = False
            if hasattr(self, "synchronous"):
                if action in self.synchronous:
                    isSync = True

            if isSync:
                self.syncID.append(uniqueID)
                while True:
                    sleep(0.1)
                    current = self.syncID[0]
                    if uniqueID == current:
                        break
                
            self.exec(action, metaData)
            
        except CommandReturnMessage:
            pass

        except KeyboardInterrupt as err:
            raise err
        
        except BaseException as err:
            applogE(f"command {self.name} catched en error", traceback.format_exc())
            return {
                "status": None,"response":"command_execution_catched_error"
            }

        if isSync:
            self.syncID.pop(0)

        return self.__set_res()

    @abstractmethod
    def exec(self, action:str, metaData:dict) -> exec_command_returned_dict:
        """
        ### Explanation:
        this method is execute specific action.
        ### Args:
        @action: string, action name to execute inside the command class, required.
        @metaData: dict, any additional data want to pass, default: empty dict.
        ### return:
        dict, return the response from executed action @status : True if all running good else False if command execution didn't occured as intended or None for exceptions or undefined action, @response for passed returned data it can be empty, e.g. { "status":True|False|None, "response":any }. 
        """
        pass
    
    def __set_default_res(self):
        self.status = None
        self.res = "command_action_not_found" 
    
    def __set_res(self) -> exec_command_returned_dict:
        res = {
            "status":self.status,
            "response":self.res
        }
        self.__set_default_res()
        return res

    def returnCMres(self, status:bool, response:Any):
        if (not type(status) is bool):
            raise Exception()
        self.status = status
        self.res = response
        raise CommandReturnMessage()

    @abstractmethod
    def initilize(self) -> None:
        """This abstract method it should be defined by the child class that inherit this BaseCommand class, and is invoked when the class is instantiated.
        """
        pass