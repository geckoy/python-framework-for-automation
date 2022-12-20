from services.general.BaseService import BaseService
from App.Helpers import *
from App.abstract.process_managment.BaseProcesses import BaseProcesses
class tester(BaseService):
    events = [
        "app_loop_before",
        "app_loop_process",
        "app_loop_after"
    ]

    def initilize(self) -> None:
        if isDebug():   
            self.tester_counter = 0
    

    def run(self, event:str):
        if isDebug():
            if event == "app_loop_before":
                # print([ e.e_name for e in self.events.get_events()])
                # debugMsg("tester loop_before")
                self.tester_counter += 1
            if event == "app_loop_process":
                # debugMsg("tester loop_process")
                pass
            if event == "app_loop_after":
                # debugMsg("tester loop_after")
                print(self.tester_counter)
                if self.tester_counter == 20:
                    # c = self.commands.exec_command("manage_app","check_app")
                    # print(f"App check is {c}")
                    print("raising Exception")
                    print(getApplication(True).commands.exec_command("manage_app","stop_app"))

    def app_close(self):
        if isDebug():
            pass