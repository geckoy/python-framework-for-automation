from http.client import HTTPConnection
import json
from App.Helpers import *
from http.server import HTTPServer
from http.client import HTTPMessage
from commands.serverHandler import server_Handler
import re
from commands.BaseCommand import BaseCommand
from typing import Any
from App.abstract.process_managment.BaseProcesses import BaseProcesses
class commands:
    def __init__(self) -> None:
        self.app = getApplication(True)
        if not self.app: raise Exception(f"No Application has been detected in {__file__}")
        self.app.commands = self
        self.port = env("APP_COMMAND_PORT")
        self.address = env("APP_COMMAND_HOST")
        self.SERVER : HTTPServer = HTTPServer((self.address,self.port), server_Handler(self.retreive_http_request))
        self.SERVER.timeout = 0.01
        self.commands : list[BaseCommand] = []
        self.initilize()

    def initilize(self):
        """
        ### Explanation:
        This method is executed after server and commands bag being saved
        ### Args:
        accept no args
        ### return:
        None
        """
        debugMsg("Loading Commands ...")
        commandsToregister = []
        ListenersfilePath = "commands/command"
        filesNames = [ f.replace(".py", "") for f in os.listdir(ListenersfilePath) if not re.match('__.*__', f)]
        for n in filesNames:
            filePath = (ListenersfilePath.replace("/",".") + (("." + n)))
            m = importlib.import_module(filePath)
            cls = getattr(m, n)
            commandsToregister.append({
                "name":n,
                "filePath":filePath,
                "cls":cls
            })
        
        for BaseP in BaseProcesses.inheritors_classes():
            rn = BaseP.processname
            n = f"{rn}Commands"
            filePath= f"{rn}Process.general.{n}"
            m = importlib.import_module(filePath, n)
            cls= getattr(m,n)
            commandsToregister.append({
                "name":n,
                "filePath":filePath,
                "cls":cls
            })

        for c in commandsToregister:
            cls = c["cls"];n = c["name"];filePath=c["filePath"]
            if issubclass(cls, BaseCommand):
                self.add_command(cls(n, filePath, self.app))
                debugMsg("loaded Command : {}", filePath)

    def check_new_request(self) -> None:
        self.SERVER.handle_request()

    @classmethod
    def send_http_req(self, data, port, host) -> bool|None:
        r = None
        while True:
            try:
                PORT = port
                conn = HTTPConnection(f"{host}:{PORT}")
                headers = {'Content-type': 'application/json'}
                json_data = json.dumps(data)
                conn.request('POST', '/', json_data, headers)
                response = conn.getresponse()
                conn.close()
                res : dict = json.loads(response.read().decode())
                r = res.get("message")
                break

            except TimeoutError:
                continue

            except:
                break
        return r
                
    def process_return_msg(self, message):
        tp = type(message)
        if tp is dict:
            message = json.dumps(message) 
            message = "type:dict|" + message
        
        elif tp is bool:
            message = "True" if message else "False"
            message = "type:bool|" + message
        
        elif message is None:
            message = "type:NoneType|None"

        return {
            "message" : message
        }

    def retreive_http_request(self, headers:HTTPMessage, messageBody:client_command_mesg_Body) -> Any:
        """
        ### Explanation:
        this method is executed when receiving post request from the server and return data of the executed command as dict 
        ### Args:
        @headers: object, headers of the http request, required.
        @messageBody: dict, client build message body.
        ### return:
        bool, False for undefiend command.
        None, for exception occured.
        dict, for command response.  
        """
        try:
            res = self.exec_command(**messageBody)
            res = res if res != None else False
        except KeyboardInterrupt as err:
            raise err

        except:
            res = None
            applogE("Client command catched error : ", traceback.format_exc())
                
        return self.process_return_msg(res)
    
    def exec_command(self, cmName:str, action:str, metaData:dict = {}) -> exec_command_returned_dict|None:
        """
        ### Explanation:
        this method is the protal for all commands, with it you can execute any command.
        ### Args:
        @cmName: string, command name, required.
        @action: string, action name to execute inside the command class, required.
        @metaData: dict, any additional data want to pass, default: empty dict.
        ### return:
        dict, return the response from executed action @status : True if all running good else False if command execution didn't occured as intended or None for exceptions or undefined action, @response for passed returned data it can be empty, e.g. { "status":True|False|None, "response":any }. 
        None, for undefied command
        """
        res = None
        command = self.get_command(cmName)
        if command:
            res = command.execC(action, metaData)

        return res

    def add_command(self, command:BaseCommand) -> None:
        """
        ### Explanation:
        add command into the bag
        ### Args:
        @command: object, commnand object, required.
        ### return:
        None
        """
        self.commands.append(command)
    
    def get_command(self, n:str) -> BaseCommand|None:
        """
        ### Explanation:
        get the command with spcific name
        ### Args:
        @n: string, name of the command want to get, required.
        ### return:
        object, command object
        """
        command = None
        for c in self.commands:
            if c.name == n:
                command = c
                break
        return command

    def __del__(self):
        if hasattr(self, "SERVER"):
            self.SERVER.server_close()

#* STATE the problem clearly:
#============================
# commands script that handles user commands and internal app commands
#
#* try to cover all eadge cases:
#=============================== 
#  1. the user got the ability to send commands to the app
#  2. the app has the ability to send commands to itself
#  3. Having each action its own command file.
# 
# 
# 
# 
#  #