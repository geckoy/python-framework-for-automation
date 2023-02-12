from vpsampleProcess.general.BaseVpsample import BaseVpsample
from vpsampleProcess.general.vpsampleArgs import vpsampleArgs
class vpsample(BaseVpsample, vpsampleArgs):
    parallel = True
    def initilize(self, id) -> None:
        self.setProperties()


    def run(self):
        print("vpsample running :", self.counter)
        self.counter += 1
                
    def app_close(self):
        pass