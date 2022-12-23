from vpsampleProcess.general.BaseVpsample import BaseVpsample

class sample(BaseVpsample):
    events = [
        "app_loop_before"
    ]
    def initilize(self, *args) -> None:
        pass


    def run(self, event:str):
        pass
    
    def app_close(self):
        pass