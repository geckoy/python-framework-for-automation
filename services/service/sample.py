from services.general.BaseService import BaseService
class sample(BaseService):
    events = [
        "app_loop_before",
        "app_loop_after",
    ]
    def initilize(self, *args) -> None:
        pass


    def run(self, event:str):
        # self.log_success("Catched success on sample service ", event)
        print(event)
        
    def app_close(self):
        pass