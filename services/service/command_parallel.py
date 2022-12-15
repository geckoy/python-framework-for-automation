from services.general.BaseService import BaseService

class command_parallel(BaseService):
    def run(self, event:str):
        print("parallel")

    def __del__(self):
        pass