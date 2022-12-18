from services.general.BaseService import BaseService
from App.Helpers import * 
from commands.commands import commands
class command(BaseService):
    events = [
        "app_starting",
        "app_loop_after"
    ]

    def run(self, event:str):
        if event == "app_starting":
            self.cm = commands()
            
        elif event == "app_loop_after":
            self.cm.check_new_request()
        
    def __del__(self):
        pass