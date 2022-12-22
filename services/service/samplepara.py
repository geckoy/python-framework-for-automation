from services.general.BaseService import BaseService
from time import sleep
class samplepara(BaseService):
    parallel = True

    def initilize(self, *args) -> None:
        self.set_status("service samplepara got initilized")
        self.counter = 0
        self.set_status("service samplepara counter created")

    def run(self):
        # self.log_success("Catched success on sample service ", event)
        self.counter += 1
        print("service samplepara counter : ", self.counter)
        self.set_status("samplepara counter incremented")
        sleep(0.5)

    def app_close(self):
        pass