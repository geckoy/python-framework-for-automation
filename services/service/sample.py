from services.general.BaseService import BaseService
from time import sleep
class sample(BaseService):
    events = [
        "app_loop_before",
        "app_loop_after",
    ]
    def initilize(self, *args) -> None:
        self.set_status("service got initilized")


    def run(self, event:str):
        # self.log_success("Catched success on sample service ", event)
        print("service event : ", event)
        sleep(0.5)
    def app_close(self):
        pass