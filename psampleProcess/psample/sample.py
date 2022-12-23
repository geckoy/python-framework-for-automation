from psampleProcess.general.BasePsample import BasePsample

class sample(BasePsample):
    events = [
        "app_loop_before"
    ]
    def initilize(self, *args) -> None:
        pass


    def run(self, event:str):
        pass
    
    def app_close(self):
        pass