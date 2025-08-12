from abc import ABC, abstractmethod
from App.Helpers import *
import datetime
import inspect
class BaseProcess(ABC):
    """
    ### Explanation:
    This abstract class is used with each process want to integrate it in BaseMultiProcessing
    ### Args:
    @args: list, arguments that will be needed by the process, required.
    ### return:
    None
    """
    def __init__(self, logger:dict, cat_name:str, name:str, *args, Parallel_args:dict = None) -> None:
        self.logger = logger
        self.categoryName = cat_name
        self.name = name
        self.__parallel_args = Parallel_args
        self.status = ""
        self.ginfo = {}
        self.set_status("Process Initilizing...")
        self.log_success("Process Initilizing...")
        # ---------------------------------------------------------------
        
        if isDebug() and hasattr(self, "parallel"):
            # ---- debugpy dev hook (only active when DEBUG_SUBPROCESS=1) ----
            cliArgs = get_cli_args()
            try:
                import debugpy
                # choose a base port or allow override via env
                base_port = int(cliArgs.get("debug_port_base", 5678))
                # make a stable / unique-ish port per process (avoid collisions)
                port = base_port + (os.getpid() % 1000)
                host = cliArgs.get("debug_host","0.0.0.0").lower()
                debugpy.listen((host, port))
                self.set_process_ginfo("debug_host", host)
                self.set_process_ginfo("debug_port", port)
                self.debugMsg(f"debugpy listening on {host}:{port} (pid={os.getpid()})")
                # Optionally wait until you attach before continuing
                # if os.environ.get("WAIT_FOR_DEBUGGER", "").lower() in ("1", "true"):
                #     print("[DEBUG] waiting for debugger to attach...")
                #     debugpy.wait_for_client()
                #     print("[DEBUG] debugger attached, continuing...")

            except Exception as e:
                print("[DEBUG] couldn't start debugpy:", e)
        # ---------------------------------------------------------------
        self.initilize(*args)
        self.set_status("Process Initilized")
        self.log_success("Process Initilized")
        
    @property
    def events(self)-> list[str]:
        """
        which events the process is listening to, this typehint is added forcebly so don't try to check it with hasattr().
        """
        return []

    @abstractmethod
    def initilize(self, *args) -> None:
        """
        ### Explanation:
        This method is executed when class is created don't try to fetch data from other processes that inherit process_management abstract concept.
        ### Args:
        @args: list, argument needed by the process, required.
        ### return:
        None
        """
        pass

    @abstractmethod
    def run(self, event:str) -> None:
        """
        ### Explanation:
        this method meant to execute the process in interval way.
        ### Args:
        @event: string [ any event inside the listeners of events/listeners], this sepcify which event been executed and called the service, required.
        ### return:
        None
        ### Note:
        the @event arg it will be ommitted when running in parallel so be sure to remove it when running the process in parallel. 
        """
        pass
    
    @abstractmethod
    def app_close(self):
        """
        ### Explanation:
        abstarct magic method executed when removing the class object from mem.
        ### Args:
        accept no args.
        ### return:
        None
        """
        pass
    
    def log_success(self, Title:str, *args, Epath:str = None):
        """This Method Logs success in the process log file.

        Args:
            Title (str): your log text
            Epath (str, optional): path of the log file. Defaults to None.
        """
        frame_info = inspect.stack()[1]  # Get information about the caller (1 level up in the stack)
        file_path = frame_info.filename   # Extract the file path from the frame information
        line_number = str(frame_info.lineno)
        if Epath == None:
            Epath=os.path.abspath(file_path)+":"+line_number
        logS(getLogging(self.logger["name"], self.logger["path"]), Title, *args, Epath = Epath )

    def log_error(self, Title:str, *args, Epath:str = None):
        """This Method Logs error in the process log file.

        Args:
            Title (str): your log text
            Epath (str, optional): path of the log file. Defaults to None.
        """
        frame_info = inspect.stack()[1]  # Get information about the caller (1 level up in the stack)
        file_path = frame_info.filename   # Extract the file path from the frame information
        line_number = str(frame_info.lineno)
        if Epath == None:
            Epath=os.path.abspath(file_path)+":"+line_number
        logE(getLogging(self.logger["name"], self.logger["path"]), Title, *args, Epath = Epath )
    
    def debugMsg(self, message:str, *args, Force:bool = False, specificFile:str =None) -> None:
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
        debugMsg(message, *args, Force=Force, specificFile={"name":self.logger['name'], "path":self.logger['path']})

    def exec_command(self, cmName:str, action:str, metaData:dict = {}, *, START_MSG = None, END_MSG = None) -> Any|None:
        if START_MSG != None: self.set_status(START_MSG)
        if hasattr(self, "parallel"):
            return exec_command(cmName, action, metaData)
        else:
            app = getApplication(True)
            if app == None: return None
            app.commands.exec_command(cmName, action, metaData)
        if END_MSG != None: self.set_status(END_MSG)
    
    def set_status(self, stats:str):
        """when you invoke This method with its stats param, it will register this stats into 
        memory of the app, you can check on stats using exec_command helper function or check it
        on the Pyffa gui. 

        Args:
            stats (str): type a text describing the stats of your current process.
        """
        if isinstance(stats, str):
            stats = stats + "|" + str(datetime.datetime.now().strftime("%H:%M:%S-%d"))
            if hasattr(self, "parallel"):
                self.__parallel_args["status"] = stats
            else:
                self.status = stats
    
    def stop(self):
        self.exec_command(f"{self.categoryName}Commands", f"stop_{self.categoryName}", {f"{self.categoryName}_name":self.name, "timeout":1})
    
    def set_process_ginfo(self, name, val):
        """This method track process attributes and keep them up to date with pyffa memory 
        you can check on them using exec_command.

        Args:
            name (_type_): name of the attribute. 
            val (_type_): value of the attribute.
        """
        if isinstance(val, str) or isinstance(val, int) or isinstance(val, list):
            val = str(val)
            if hasattr(self, "parallel"):
                if not "ginfo" in self.__parallel_args: self.__parallel_args["ginfo"] = {}
                self.__parallel_args["ginfo"]= {**self.__parallel_args["ginfo"], name:val}
            else:
                self.ginfo[name] = val