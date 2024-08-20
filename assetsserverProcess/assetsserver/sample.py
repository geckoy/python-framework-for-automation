from assetsserverProcess.general.BaseAssetsserver import BaseAssetsserver

class sample:#(BaseAssetsserver):
    events = [
        "app_loop_before"
    ]
    def initilize(self, *args) -> None:
        pass


    def run(self, event:str):
        pass
    
    def app_close(self):
        pass