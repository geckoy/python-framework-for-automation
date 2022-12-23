from vpsampleProcess.general.BaseVpsample import BaseVpsample

class vpsample(BaseVpsample):
    parallel = True
    def initilize(self, id) -> None:
        print(id)
        self.counter = 0


    def run(self):
        print("vpsample running :", self.counter)
        self.counter += 1
                
    def app_close(self):
        pass