from services.general.BaseService import BaseService
from App.Helpers import *
class tester(BaseService):
    events = [
        "app_starting",
        "app_loop_before",
        "app_loop_process",
        "app_loop_after"
    ]
    def run(self, event:str):
        if isDebug():
            if event == "app_starting":
                # debugMsg("tester Starting")
                self.app.counter = 0
            if event == "app_loop_before":
                # debugMsg("tester loop_before")
                self.app.counter += 1
            if event == "app_loop_process":
                # debugMsg("tester loop_process")
                pass
            if event == "app_loop_after":
                # debugMsg("tester loop_after")
                print(self.app.counter)
                if self.app.counter == 20:
                    print("raising Exception")
                    self.app.close()
    def __del__(self):
        if isDebug():
            print("tester Closed")