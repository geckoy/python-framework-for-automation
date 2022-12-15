# Modules
from App.UserExceptions import * 
import sys
from loguru import logger
import re
import os
from time import * 
from peewee import SqliteDatabase
from uuid import uuid4 as uid
from inspect import getframeinfo, stack
import traceback
import importlib
# Helpers
def debugMsg(message:str, *args, Force:bool = False, specificFile:str =None) -> None:
    """
    ### Explanation:
    This function used to print your message into console if the app is running in debug mode.
    ### Args:
    @message: can be String, is used to hold the message you want to log, required.  
    @Force: can be bool, used to force debug, default: False.
    @specificFile: can be String {"name":"name to register in memory", "path":"temp/logs/FileName.log", "rotation":"1 MB"}, used to set specific file to write the debug message helpful with parallel, default: None.
    @args: can be dataType, is a list param that will be formatted inside the @message string, default: empty list.
    ### return: 
    None
    ### Examples: 
    from App.Helpers import *\n
    debugMsg("Hello {}!", "World")
    """
    ifExec = isDebug() if not Force else True
    if ifExec:
        if specificFile == None:
            applog(message, *args, event="debug") 
        else:
            l = getLogging(**specificFile)
            log(l, *args, event="debug")
        if specificFile == None:
            applog(message, *args, event="debug", cli=True) 

def isDebug():
    """
    ### Explanation:
    Checks whether the app is running in debug mode if no app is instantiated it will return False
    ### return:
    bool, True or False for app debug if no app is running it will be False.
    """
    app = getApplication(True)
    if app != None:
        return app.DEBUG
    else: 
        return False

def getApplication( OnlyMemory :bool = False, *, debug:bool = False):
    """
    ### Explanation:
    Helper function meant instantiate the application class and its saved into the memory, any subsequent invokes will serve from it. 
    ### Args:
    @OnlyMemory: can be [ True | False ], this param specify if you want to only pull the app from mem without instantiating it, default: False.
    ### return: 
    object, application from app.py
    None if OnlyMemory is True and no app is retreived
    """
    default = None
    mem = memory()
    result = mem.get("application") if mem.get("application", default) else default
    if not OnlyMemory:
        if result == default:
            from app import application
            application(debug)
            result : application = memory().get("application", default)
    
    return result

def getAppLogging(isCli = False) -> logger:
    """
    ### Explanation:
    This function used to serve app logging.
    ### Args:
    @isCli: can be bool, this param is used to specify if you want to log the message to cli, default: False. "this means it will be printed in console"
    ### return: 
    object, logger from loguru. 
    """
    if isCli:
        loggingName = "apploggercli";loggingPath = sys.stdout 
    else: 
        loggingName = "applogger";loggingPath = "temp/logs/app.log" 
    return getLogging(loggingName, loggingPath)

def getLogging(name, path, rotation = "1 MB") -> logger :
    """
    ### Explanation:
    This function instantiate the loguru class to make logging messages pretty, works for both files and cli.
    ### Args:
    @name: can be String, name of the logging instance that you want to be registered in memory, required.
    @path: can be [ String | sys.stdout | file-like object | pathlib.Path | callable | coroutine function | logging.Handler ], this param used to specify where loguru instance should log the message, required.
    @rotation: can be String, param used to specify when to rotate files, default: "1 MB".
    ### return: 
    object, logger from loguru. 
    """
    response = None
    response = memory().get(name, False)
    registerMem = (type(path) == "string")
    # * global config 
    loggerConfig = {}
    loggerConfig["format"]='<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> - <level>{message}</level>'
    
    if response: return response
    
    logger.remove()
    # * the config for file
    if registerMem: loggerConfig["rotation"] = rotation
    logger.add(path, **loggerConfig)
    response = logger       

    if registerMem: add2memory(**{name:logger})

    return response

def memory(purpose :str = "get", *args, __mem : dict = {}, **kwargs ) -> dict | None:
    """
    ### Explanation:
    This function used to store data in static param dict, used as memory to store data.
    ### return:
    dict, the store data key-value.\n
    None, if some other purpose have made like adding or removing.
    """
    response = None
    match purpose :
        case "get":
            response = __mem 
        case "add":
            __mem.update({**kwargs})
        case "remove":
            for k in args:
                try:
                    del __mem[k]
                except: 
                    pass
    
    return response

def add2memory(**kwargs):
    if kwargs:
        memory("add",**kwargs)

def remove4rmemory(*args):
    if args:
        memory("remove", *args) 

def get_os_distro() -> str:
    """
    ### Explanation:
    this function return current os.
    ### return:
    string: name of the os system linux or undefined "linux is the only supported os".
    """
    import platform
    OS = platform.platform()
    return "linux" if re.match("linux", OS, re.IGNORECASE) else "Undefined"

def start_application(supervisor:str = "cli", debug :bool = False) -> None:
    """
    ### Explanation:
    This function execute the start.py file which launches the application
    ### Args:
    @supervisor: can be string [ "cli" | "pm2" ], is used to define which supervisor will be used, default: cli.
    @debug: can be bool [ True | False ], is used to set launching mode of app, default: False.
    ### return:
    None
    """
    isDebug = "True" if debug else "False"
    match supervisor:
        case "cli":
            print("Running App with SuperVisor cli")
            os.system("python start.py {}".format(isDebug))
        case "pm2":
            print("Running App with SuperVisor pm2")
            return os.system(f"pm2 start start.py --name MMAPI -- {isDebug}")
        case _:
            raise undefinedArgs("Please specify a supervisor")

def getDatabaseConnection(dbDriver = "mysql", *, debug:bool = False)-> SqliteDatabase:
    """
    This function it serves the db connection for peewee BaseModel.
    """
    db = memory().get("db", False)
    debugMsg("Creating Database Connection {}", ( "'already Created'" if db else "") , Force = debug)
    if not db: 
        debugMsg("Database Connection Created", Force=debug)
        db = SqliteDatabase("App/database/app.db")
        add2memory(db=db)

    return db

def applog( message:str, *args, event:str = "success", cli = False) -> None:
    """
    ### Explanation:
    This function is used to log the success or error event in app.log file.
    ### Args:
    @message: can be String, is used to hold the message you want to log, required.
    @args: can be dataType, is a list param that will be formatted inside the @message string, default: empty list.
    @event: can be String [ success | error | debug ], used to set logged message if is error or success, default: success.
    ### return:
    None
    """
    Applicationlog = getAppLogging(isCli=cli)
    log(Applicationlog,message, *args,event=event)

def log(logger:object, message:str, *args, event:str = "success") -> None:
    """
    ### Explanation:
    This function is used to log the success or error event in log file.
    ### Args:
    @logger: can be object, its the object class that manage the logging to file process, required. 
    @message: can be String, is used to hold the message you want to log, required.
    @args: can be dataType, is a list param that will be formatted inside the @message string, default: empty list.
    @event: can be String [ success | error | debug ], used to set logged message if is error or success, default: success.
    ### return:
    None
    """
    m = message.format(*args)
    f = getattr(logger, event)
    f(m)

def applogS(Title:str, *args) -> None:
    """
    ### Explanation:
    log success message into app.log
    ### Args:
    @message: can be String, is used to hold the message you want to log, required.
    @args: can be dataType, is a list param that will be formatted inside the @message string of log(), default: empty list.
    """
    l = getAppLogging()
    caller = getframeinfo(stack()[1][0])
    logS(l, Title, *args, Epath = f"{caller.filename}:{caller.lineno}")

def applogE(Title:str, *args) -> None:
    """
    ### Explanation:
    log error message into app.log
    ### Args:
    @Title: can be String, is used to hold the message Title you want to log, required.
    @args: can be dataType, is a list param that will be formatted inside the @message string of log(), default: empty list.
    """
    l = getAppLogging()
    caller = getframeinfo(stack()[1][0])
    logE(l, Title, *args, Epath=f"{caller.filename}:{caller.lineno}")

def logE(logger:object, Title:str, *args, Epath:str = None):
    """
    ### Explanation:
    log success message into log file
    ### Args:
    @message: can be String, is used to hold the message you want to log, required.
    @args: can be dataType, is a list param that will be formatted inside the @message string, default: empty list.
    """
    if Epath != None:
        path = Epath
    else:
        caller = getframeinfo(stack()[1][0])
        path = f"{caller.filename}:{caller.lineno}"
    _logEvent(logger, Title, *args, Epath=path, event="error")

def logS(logger:object, Title:str, *args, Epath:str = None):
    """
    ### Explanation:
    log error message into log file
    ### Args:
    @message: can be String, is used to hold the message you want to log, required.
    @args: can be dataType, is a list param that will be formatted inside the @message string, default: empty list.
    """
    if Epath != None:
        path = Epath
    else:
        caller = getframeinfo(stack()[1][0])
        path = f"{caller.filename}:{caller.lineno}"
    _logEvent(logger, Title, *args, Epath=path, event="success")

def _logEvent(logger:object, Title:str, *args, Epath, event):
    argCount = len(args) 
    identification = uid()
    additionals = ""
    if argCount > 0:
        additionals = "\n{}" * argCount
    msg = f"{identification}\n" + Title + additionals + "\nFILE PATH: {}"+ f"\n{identification}"
    log(logger, msg, *args, Epath, event=event)