class undefinedArgs(BaseException):
    """This Exception is raised when user inject false or undefined argument"""

class ApplicationCatchedError(BaseException):
    """This Exception is raised when application catch an error"""

class CommandReturnMessage(BaseException):
    """This Exception is raised when command has return response"""