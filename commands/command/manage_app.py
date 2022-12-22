from commands.BaseCommand import BaseCommand
from App.Helpers import *

class manage_app(BaseCommand):

    def exec(self, action:str, metaData:dict) -> exec_command_returned_dict:
        if action == "stop_app":
           self.stop_app()
        elif action == "check_app":
           self.check_app()
        elif action == "test":
            sleep(15)
            self.returnCMres(True, "slept well jhon")
    def check_app(self):
        self.returnCMres(True, True)

    def stop_app(self):
        self.app.close()