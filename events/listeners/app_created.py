from events.BaseListener import BaseListener
from App.abstract.process_managment.BaseProcesses import BaseProcesses
from App.Helpers import *
from os import listdir

class app_created(BaseListener):
    """
    Here where you register your abstract concept of process_management and other class instantiation.
    """
    def run(self):
        for d in listdir():
            if re.match(".*Process", d, re.IGNORECASE):
                processname = d.replace("Process", "")
                path = f"{processname}Process.general.{processname}Manager"
                importlib.import_module(path)

        classes = BaseProcesses.inheritors_classes()
        for cls in classes:
            if cls.processname == "vpsample" or cls.processname == "psample":
                if not isDebug():
                    continue
            cls()