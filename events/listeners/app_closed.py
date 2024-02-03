from events.BaseListener import BaseListener
import os
from App.Helpers import memory, stopPm2
class app_closed(BaseListener):
    
    def run(self, *args):
        self.app.events.accept_all_events("app_closed")
        if memory().get("supervisor","")=="pm2": 
            stopPm2(self.app.AppName)