from App.abstract.process_managment.BaseProcesses import BaseProcesses

class vpsampleManager(BaseProcesses):
    """
    ### Explanation:
    this class meant to be the vpsample manager for vpsample process
    vpsample stands for virtual process sample
    ### Args :
    accept no args.
    """
    processname = "vpsample"
    processespath = "vpsampleProcess/vpsample"
    processesManagerPath = "vpsampleProcess/general/vpsample"
    virtual = True
    def __init__(self) -> None:
        super().__init__()
    
    def get_vdata(self) -> list:
        vd = {
                "id":5,
                "name":"organizeuser_younes",
                "autoStart":True,
                "args":[5],
            }
        
        self.set_vdata(**vd)