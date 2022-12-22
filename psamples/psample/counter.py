from psamples.general.BasePsample import BasePsample
from App.Helpers import *

class counter(BasePsample):
    events = [
        "app_loop_before",
        "app_loop_after"
    ]

    def initilize(self, *args) -> None:
        self.tester_counter = 0
    

    def run(self, event:str):
        if event == "app_loop_before":
            # print([ e.e_name for e in self.events.get_events()])
            # debugMsg("tester loop_before")
            self.tester_counter += 1
        
        elif event == "app_loop_after":
            # debugMsg("tester loop_after")
            print(self.tester_counter)
            if self.tester_counter == 20:
                # c = self.commands.exec_command("manage_app","check_app")
                # print(f"App check is {c}")
                print("raising Exception")
                self.exec_command("manage_app","stop_app")

    def app_close(self):
        pass