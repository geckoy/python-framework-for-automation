from typing import TypedDict, Literal, Any


class client_command_mesg_Body(TypedDict):
    type : Literal["normal", "ez"]
    cmName : str
    action : str
    metaData : dict

class exec_command_returned_dict(TypedDict):
    status :bool|None
    response : Any