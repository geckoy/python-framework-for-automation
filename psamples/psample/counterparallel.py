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
        sleep(0.5)

    def app_close(self):
        pass