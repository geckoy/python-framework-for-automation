from commands.BaseCommand import BaseCommand
from App.Helpers import *
class manage_services(BaseCommand):
    def exec(self, action:str, metaData:dict) -> exec_command_returned_dict:
        if action == "start_service":
            s = self.get_specific_service(metaData)
            r = s.start()
            self.returnCMres(r, r)
        elif action == "pause_service":
            s = self.get_specific_service(metaData)
            s.pause()
            self.returnCMres(True, True)
        elif action == "unpause_service":
            s = self.get_specific_service(metaData)
            s.unPause()
            self.returnCMres(True, True)
        elif action == "stop_service":
            s = self.get_specific_service(metaData)
            s.stop()
            self.returnCMres(True, True)
    
    def get_specific_service(self, metaData:dict):
        if metaData.get("service_name","undefined") == "undefined": raise Exception("service Name undefiend")
        s = self.app.services.get_service(metaData["service_name"])
        if s == None: raise Exception("service name is not registered in our service manager")
        return s