from psampleProcess.general.BasePsample import BasePsample
from App.Helpers import *
from psampleProcess.general.psampleArgs.counterparallel import counterparallel as args
class counterparallel(BasePsample, args):
    events = [
    ]
    parallel = True
    parallelTimeout = 1
    def initilize(self, *args) -> None:
        self.setProperties()

    def run(self):
        counter = self.mycounter 
        self.set_status("psample Counter parallel mode is {}".format(counter))
        print("psample Counter parallel mode is {}".format(counter))
        self.mycounter  +=1
        # if self.mycounter == 20:
        #     self.exec_command("manage_app", "stop_app")
        # sleep(0.5)
        sleep(2)
    def app_close(self):
        pass