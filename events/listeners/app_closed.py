from events.BaseListener import BaseListener
import os
from App.Helpers import memory, stopPm2, killGrandChildren
class app_closed(BaseListener):
    
    def run(self, *args):
        self.app.events.accept_all_events("app_closed")
        spfEnv = memory().get("specific_env","")
        if memory().get("supervisor","")=="pm2": 
            stopPm2(self.app.AppName)
        killGrandChildren(spfEnv)