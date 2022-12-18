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
                # Print Services info
                debugMsg("Services Data: {}", str([ f"name: {s.name}, isParallel: {s.isParallel}" for s in self.app.services.get_services()]).replace("['","\n ").replace("']","").replace("',","\n").replace("'",""))
                
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
                    # c = self.app.commands.exec_command("manage_app","check_app")
                    # print(f"App check is {c}")
                    print("raising Exception")
                    print(self.app.commands.exec_command("manage_app","stop_app"))

    def __del__(self):
        if isDebug():
            pass