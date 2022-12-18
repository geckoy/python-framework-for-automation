from services.general.BaseService import BaseService
from App.Helpers import *
class counter(BaseService):
    events = [
        "app_starting",
        "app_loop_before"
    ]
    def run(self, event:str):
        if event == "app_starting":
            self.mycounter = 0
        elif event == "app_loop_before":
            counter = self.mycounter 
            print("Counter is {}".format(counter))
            self.mycounter  +=1

    def __del__(self):
        pass