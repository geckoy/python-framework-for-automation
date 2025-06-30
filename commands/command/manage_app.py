from commands.BaseCommand import BaseCommand
from App.Helpers import *
from App.abstract.process_managment.BaseProcesses import BaseProcesses
class manage_app(BaseCommand):
    synchronous = ["test"]
    def initilize(self) -> None:
        pass

    def exec(self, action:str, metaData:dict) -> exec_command_returned_dict:
        if action == "stop_app":
           self.stop_app()
        elif action == "check_app":
           self.check_app()
        elif action == "test":
            print("received request")
            sleep((5))
            self.returnCMres(True, "slept well jhon")
        elif action == "get_running_processes":
            res = [x.processname for x in BaseProcesses.inheritors() if x.processname in dir(self.app)]
            self.returnCMres(True, res)

        elif action == "get_subprocesses_names":
            proc:BaseProcesses = getattr(self.app, metaData["process_name"])
            res = proc.get_all_names()
            self.returnCMres(True, res)
    
    def check_app(self):
        self.returnCMres(True, True)

    def stop_app(self):
        self.app.closeFlag = True