from App.abstract.process_managment.BaseProcesses import BaseProcesses

class assetsserverManager(BaseProcesses):
    """
    ### Explanation:
    this class meant to be the assetsserver manager for assetsserver process
    assetsserver stands for virtual process sample
    ### Args :
    accept no args.
    """
    processname = "assetsserver"
    processespath = "assetsserverProcess/assetsserver"
    processesManagerPath = "assetsserverProcess/general/assetsserver"
    
    def __init__(self) -> None:
        super().__init__()