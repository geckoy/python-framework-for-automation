from App.Helpers import *
from App.eventsApi import events
from services.general.services import services
from events.events import events as ev
from typing import Callable
class application:
    def __init__(self, debug:bool = False) -> None:
        # Register App in mem
        add2memory(application=self)
        # Set app debug mode & operating sys
        self.DEBUG = debug;debugMsg("debug mode is Activated");self.OS = get_os_distro()
        self.loopTimeout = 0.1
        self.events = events(self)
        self.services : services
        # launch creating event
        self.events.app_created()

    def initiate(self) -> None:
        """
        ### Explanation:
        This application class method meant to initilize the app processes. 
        ### Example: 
        from App.Helpers import * \n
        app = getApplication(False)\n
        app.initiate()
        """
        self.events.app_starting()
        print("Application Started ...")
        self.loop()

    def loop(self) -> None:
        debugMsg("Application loop initilize")
        while True:
            try:
                sleep(self.loopTimeout)
                self.events.app_loop_before()
                self.events.app_loop_process()
                self.events.app_loop_after()

            except KeyboardInterrupt:
                break

            except BaseException as err:
                applogE("Application loop catched an error : ", traceback.format_exc())
                continue

    def close(self):
        raise KeyboardInterrupt

    def __del__(self) -> None:
        self.events.app_closed()



#? State The Problem & identify inputs and outputs:
#?==================================================
#  we need a application management class, inputs: user-args | outputs: datatypes
# 
#! Try to cover all eadge cases:
#!===============================
#  4. giving stats
#
# * Done:
#=========
# 1. the starting mode of app "debug" OR "production"
# 2. starting the app using cli or pm2 or debian service
# 3. define the operating system when stating
# 4. logging exceptions