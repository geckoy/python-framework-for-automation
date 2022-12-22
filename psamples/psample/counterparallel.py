from psamples.general.BasePsample import BasePsample
from App.Helpers import *

class counterparallel(BasePsample):
    events = [
    ]
    parallel = True
    def initilize(self, *args) -> None:
        self.mycounter = 0

    def run(self):
        counter = self.mycounter 
        print("Counter is {}".format(counter))
        self.mycounter  +=1
        # if self.mycounter == 20:
        #     self.exec_command("manage_app", "stop_app")
        # sleep(0.5)

    def app_close(self):
        pass