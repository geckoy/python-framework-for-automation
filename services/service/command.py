from services.general.BaseService import BaseService
from App.Helpers import * 

class command(BaseService):
    events = [
        "app_starting"
    ]

    def run(self, event:str):
        print([ s.name for s in self.app.services.get_services()])
        
    def __del__(self):
        pass