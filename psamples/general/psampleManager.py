from App.abstract.process_managment.BaseProcesses import BaseProcesses

class psampleManager:# Don't forget to add inheritance to make it work (BaseProcesses)
    """
    ### Explanation:
    this class meant to be the psample manager for each psample
    psample stands for process sample
    ### Args :
    accept no args.
    """
    processname = "psample"
    processespath = "psamples/psample"
    processesManagerPath = "psamples/general/psample"
    
    def __init__(self) -> None:
        super().__init__()