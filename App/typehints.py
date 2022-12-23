from typing import TypedDict, Literal, Any

class apptypehints:
    """
    This class meant to set the typehints of app attributes that are added after app __init__
    """
    def __init__(self) -> None:
        from serviceProcess.general.serviceManager import serviceManager
        self.service : serviceManager

class client_command_mesg_Body(TypedDict):
    type : Literal["normal", "ez"]
    cmName : str
    action : str
    metaData : dict

class exec_command_returned_dict(TypedDict):
    status :bool|None
    response : Any