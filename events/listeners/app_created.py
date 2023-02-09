from events.BaseListener import BaseListener
from App.abstract.process_managment.BaseProcesses import BaseProcesses
from App.Helpers import *
from os import listdir

class app_created(BaseListener):
    """
    Here where you register your abstract concept of process_management and other class instantiation.
    """
    def run(self, *args):
        specificProcess = False if len(args) == 0 else args[0]
        classes = BaseProcesses.inheritors_classes()
        for cls in classes:
            if specificProcess:
                if not cls.processname in specificProcess:
                    continue
            if cls.processname == "vpsample" or cls.processname == "psample":
                if not isDebug():
                    continue
            cls()