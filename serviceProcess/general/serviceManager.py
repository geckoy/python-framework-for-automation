from App.Helpers import *
from App.abstract.process_managment.BaseProcesses import BaseProcesses
class serviceManager(BaseProcesses):
    """
    ### Explanation:
    this class meant to be the service manager for each service
    ### Args :
    accept no args.
    """
    processname = "service"
    processespath = "serviceProcess/service"
    processesManagerPath = "serviceProcess/general/service"
    
    def __init__(self) -> None:
        super().__init__()