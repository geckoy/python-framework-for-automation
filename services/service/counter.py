from services.general.BaseService import BaseService
from App.Helpers import *
class counter(BaseService):
    events = [
        "app_loop_before"
    ]
    parallel = True
    def initilize(self) -> None:
        self.mycounter = 0

    def run(self):
        counter = self.mycounter 
        print("Counter is {}".format(counter))
        self.mycounter  +=1
        sleep(0.5)

    def app_close(self):
        pass