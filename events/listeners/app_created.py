from events.BaseListener import BaseListener
from services.general.servicesManager import servicesManager
from App.Helpers import *
from psamples.general.psampleManager import psampleManager
from vpsamples.general.vpsampleManager import vpsampleManager
class app_created(BaseListener):
    """
    Here where you register your abstract concept of process_management and other class instantiation.
    """
    def run(self):
        servicesManager() 
        if isDebug():
            # psampleManager()
            vpsampleManager()