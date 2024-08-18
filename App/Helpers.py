# Modules
from App.UserExceptions import * 
import sys
from loguru import logger
import re
import json
import subprocess
import os
from time import * 
from peewee import SqliteDatabase, MySQLDatabase
from uuid import uuid4 as uid
from inspect import getframeinfo, stack
from App.typehints import *
import traceback
import importlib
from os import listdir
# Helpers
def debugMsg(message:str, *args, Force:bool = False, specificFile:dict =None) -> None:
    """
    ### Explanation:
    This function used to print your message into console if the app is running in debug mode.
    ### Args:
    @message: can be String, is used to hold the message you want to log, required.  
    @Force: can be bool, used to force debug, default: False.
    @specificFile: can be dict {"name":"name to register in memory", "path":"temp/logs/FileName.log", "rotation":"1 MB"}, used to set specific file to write the debug message helpful with parallel, default: None.
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
            log(l, message, *args, event="debug")
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

def getApplication( OnlyMemory :bool = False, *, debug:bool = False, supervisor:str=None, **kwargs):
    """
    ### Explanation:
    Helper function meant instantiate the application class and its saved into the memory, any subsequent invokes will serve from it. 
    ### Args:
    @OnlyMemory: can be [ True | False ], this param specify if you want to only pull the app from mem without instantiating it, default: False.
    @supervisor: string cli | pm2, this param specify whether we are using pm2 or cli to execute our code, default: None.
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
            application(debug,supervisor, **kwargs)
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
    return "linux" if re.match("linux", OS, re.IGNORECASE) else ("windows" if re.match("windows", OS, re.IGNORECASE) else None)

def start_application(supervisor:str = "cli", debug :bool = False, **kwargs) -> None:
    """
    ### Explanation:
    This function execute the startpyffa.py file which launches the application
    ### Args:
    @supervisor: can be string [ "cli" | "pm2" ], is used to define which supervisor will be used, default: cli.
    @debug: can be bool [ True | False ], is used to set launching mode of app, default: False.
    @kwargs: app sepcific arguments.
    ### return:
    None
    """
    additionals= ""
    for k,v in kwargs.items():
        if v: additionals += f" {k}=" +v
    isDebug = "True" if debug else "False"
    match supervisor:
        case "cli":
            print("Running App with SuperVisor cli")
            os.system("python startpyffa.py {} cli{}".format(isDebug, additionals))
        case "pm2":
            print("Running App with SuperVisor pm2")
            appName= env("APP_NAME")
            return os.system(f"pm2 start startpyffa.py --name {appName} -- {isDebug} pm2{additionals}")
        case _:
            raise undefinedArgs("Please specify a supervisor")

def getDatabaseConnection(dbDriver = "mysql", *, debug:bool = False, **kwargs)-> SqliteDatabase|MySQLDatabase:
    """
    This function it serves the db connection for peewee BaseModel.
    """
    db = memory().get("db", False)
    debugMsg("Creating Database Connection {}", ( "'already Created'" if db else "") , Force = debug)
    if not db: 
        debugMsg("Database Connection Created", Force=debug)
        db = SqliteDatabase(kwargs.get("dbpath")) if not dbDriver == "mysql" else MySQLDatabase(kwargs.get("mysqldbname"),user=kwargs.get("mysqldbun"), host=kwargs.get("mysqldbhost"), password=kwargs.get("mysqldbpw"))
        add2memory(db=db)

    return db

def getEnvDB(debug:bool=False)-> SqliteDatabase|MySQLDatabase:
    """This function return instance of db connection according to environment variables.
    ### Example#1
    >>> from App.Helpers import getEnvDB
    >>> db = getEnvDB()

    ## Args:
        @debug (``bool``, optional): whether to log the connection steps in default app logging file or not. Defaults to ``False``.

    ## Returns:
        ``SqliteDatabase|MySQLDatabase``: database connection.
    """
    return getDatabaseConnection( dbDriver=env("APP_DATABASE"),dbpath=env("DB_LOCATION","App/database/app.db"), mysqldbname=env("MYSQL_DATABASE_NAME"), mysqldbun=env("MYSQL_USERNAME"), mysqldbhost=env("MYSQL_ADDRESS"), mysqldbpw=env("MYSQL_PASSWORD"), debug=debug)

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

def exec_command(cmName:str, action:str, metaData:dict = {}):
    """
    ### Explanation:
    This function execute command using socket connection to the app command listener.
    ### Args:
    @cmName: string, command file name to execute, required.
    @action: string, action to execute of specific command file, required.
    @metaData: dict, additional data to be passed, default: empty dict.
    @type: string, normal or ez command, default:normal.
    ### return:
    bool, False for undefiend command.\n
    None, for exception occured.\n
    dict, for command response.\n
    "app_is_closed", when app is closed.\n
    ### Note:
    The dict response can also have states, it responses from execution @status : True if all running good else False if command execution didn't occured as intended or None for exceptions or undefined action, @response for passed returned data it can be empty, e.g. { "status":True|False|None, "response":any }.  
    """
    from commands.commands import commands
    cmres:str = commands.send_http_req({ "cmName": cmName,"action":action, "metaData":metaData }, port=env("APP_COMMAND_PORT"), host=env("APP_COMMAND_HOST"))
    if cmres == None: 
        cmres ="app_is_closed"
    else:
        type = cmres.split("|")[0]
        msg = cmres.split("|",1)[1]
        if "bool" in type:
            cmres = bool(msg)
        elif "dict" in type:
            cmres = json.loads(msg)
        elif "NoneType" in type:
            cmres = None

    return cmres 

def milli(sec:int= 0, start_milli:int=None):
    """
    ### Explanation
    This function return current milli or the current milliseconds with added seconds.
    ### Args:
    @sec: int, which is the seconds you want to add to the current milliseconds if zero nothing will be added and returns current milli, default: 0.
    ### return:
    int, milliseconds of current moment or future time.
    """
    if start_milli != None:
        current = start_milli + (sec * 1000)
    else:
        current = (time() + sec)* 1000
    return round(current)

def env(name:str = "", defaultVal = "undefined"):
    """
    ### Explanation:
    return enviromment variables
    ### Args:
    @name: string, name of the env variable, default: empty.
    @defaultVal: string, value to return if env var not found, default:undefined.
    ### return:
    data type of env if found else return defaultVal if setted else throw KeyError.   
    """
    with open(memory().get("specific_env","settings.json"), "r") as settings:
        envs = (json.load( settings ))
    return envs.get(name, defaultVal) if not defaultVal == "undefined" else envs[name]

def Dbmigration(purpose:str="runAll", specific:list=[]) -> None:
    """This function run|drop|refresh migrations on environment database.
    ### Example#1
    execute migration on all tables.
    >>> from App.Helpers import Dbmigration
    >>> Dbmigration("refreshAll")
    
    ### Example#2
    execute migration on specific tables
    >>> from App.Helpers import Dbmigration
    >>> from App.database.models import settings, users
    >>> Dbmigration("run", [settings, users])

    ## Args:
        @purpose (``str``, optional): type of migration to execute whether to ```dropAll```, ``runAll``, ``refreshAll`` "the refreshAll purpose first drops all tables than repopulate them", and also you can execute migration using specific models by only removing the ``All`` from commands above and adding the second parameter @specific, see example#2. Defaults to ``"runAll"``.
        @specific (``list[BaseModel]``, optional): execute migration on specific models. Defaults to ``[]``.

    ## Returns:
        ``None``: default.
    """
    from App.database.BaseModel import BaseModel
    db = getEnvDB()
    tables = BaseModel.inheritors_classes()
    match purpose:
        case "runAll":
            #This purpose add non existing tables in database.
            if len(tables) > 0: db.create_tables(tables)
        case "dropAll":
            #This purpose drop all existing tables in database.
            if len(tables) > 0: db.drop_tables(tables)
        case "refreshAll":
            #This purpose drop all existing tables in database and add new ones.
            if len(tables) > 0:
                db.drop_tables(tables)
                db.create_tables(tables)
        case "run":
            #This purpose add non existing specific tables in database.
            if len(specific) > 0: db.create_tables(specific)
        case "drop":
            #This purpose drop existing specific tables in database.
            if len(specific) > 0: db.drop_tables(specific)
        case "refresh":
            #This purpose drop specific existing tables in database and re-add.
            if len(specific) > 0:
                db.drop_tables(specific)
                db.create_tables(specific)
    return None

def killGrandChildren(self, specificEnv:str = ""):
    operatingsys = get_os_distro()
    if operatingsys == "linux":
        sleep(1)
        command = 'pkill -9 -f "python .*startpyffa\.py.*"' if len(specificEnv) == 0 else 'pkill -9 -f "python .*startpyffa\.py.*specific_env={}'.format(specificEnv)
        os.system(command)

def stopPm2(appName):
    os.system(f"pm2 stop {appName}")