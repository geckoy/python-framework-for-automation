from App.abstract.process_managment.BaseProcess import BaseProcess

class vpsample(BaseProcess):
    parallel = True
    def initilize(self, id) -> None:
        print(id)
        self.counter = 0


    def run(self):
        print("vsample running :", self.counter)
        self.counter += 1
                
    def app_close(self):
        pass