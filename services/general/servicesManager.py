from App.Helpers import *
from services.general.service import service
from App.abstract.process_managment.BaseProcesses import BaseProcesses
class servicesManager(BaseProcesses):
    """
    ### Explanation:
    this class meant to be the service manager for each service
    ### Args :
    accept no args.
    """
    processname = "service"
    processespath = "services/service"
    processesManagerPath = "services/general/service"
    
    def __init__(self) -> None:
        super().__init__()