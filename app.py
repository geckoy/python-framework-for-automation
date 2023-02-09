from App.Helpers import *
from App.eventsApi import events
from events.events import events as ev
from commands.commands import commands
from App.typehints import apptypehints
class application(apptypehints):
    def __init__(self, debug:bool = False, specific_processes:str = "") -> None:
        super().__init__()
        # Register App in mem
        add2memory(application=self)
        # Set app important classes and properties
        self.DEBUG = debug;debugMsg("debug mode is Activated");self.OS = get_os_distro()
        self.loopTimeout = 0.01
        self.eventsApi = events(self)
        self.events : ev = ev()
        self.commands : commands = commands()
        # launch creating event
        self.eventsApi.app_created(specific_processes)

    def initiate(self) -> None:
        """
        ### Explanation:
        This application class method meant to initilize the app processes. 
        ### Example: 
        from App.Helpers import * \n
        app = getApplication(False)\n
        app.initiate()
        """
        print("Application Started ...")
        self.loop()

    def loop(self) -> None:
        debugMsg("Application loop initilize")
        while True:
            try:
                sleep(self.loopTimeout)
                self.eventsApi.app_loop_before()
                self.eventsApi.app_loop_process()
                self.eventsApi.app_loop_after()
                self.commands.check_new_request()
            except KeyboardInterrupt:
                break

            except BaseException as err:
                applogE("Application loop catched an error : ", traceback.format_exc())
                continue
        self.eventsApi.app_closed()
        
    def close(self):
        raise KeyboardInterrupt

    def __del__(self) -> None:
        pass