from App.Helpers import *
from events.BaseListener import BaseListener
from events.event import event
from typing import Callable
class events:
    """
    ### Explanation:
    This class is used to manage the events 
    ### Args:
    accept no args.
    """
    def __init__(self) -> None :
        self.app = getApplication(True)
        if not self.app: raise Exception(f"No Application has been detected in {__file__}")
        self.events = []
        self.initilize()
        self.app.exec_event : Callable[[str], None] = self.run

    def initilize(self) -> None:
        """
        ### Explanation:
        This method is executed after app and events bag being saved
        ### Args:
        accept no args
        ### return:
        None
        """
        debugMsg("Loading Events ...")
        ListenersfilePath = "events/listeners"
        filesNames = [ f.replace(".py", "") for f in os.listdir(ListenersfilePath) if not re.match('__.*__', f)]
        idCounter = 0
        for n in filesNames:
            idCounter+=1
            filePath = (ListenersfilePath.replace("/",".") + (("." + n)))
            m = importlib.import_module(filePath)
            cls = getattr(m, n)
            if issubclass(cls, BaseListener):
                self.add_event(event(n, cls, filePath, self.app))
            
    def run(self, event:str) -> None:
        """
        ### Explanation:
        This is the entry point for every event launched
        ### Args:
        @event: string, name of the launched event, required.
        ### return:
        None
        """
        event = self.get_event(event)
        if event != None: 
            event.run()

    def add_event(self, event : event) -> None:
        """
        ### Explanation:
        add event into the bag
        ### Args:
        @event: object, event manager object, required.
        ### return:
        None
        """
        self.events.append(event)
    
    def get_event(self, n:str) -> event:
        """
        ### Explanation:
        get the event manager with spcific name
        ### Args:
        @n: string, name of the event manager want to get, required.
        ### return:
        object, event manager object
        """
        event = None
        for e in self.events:
            if e.e_name == n:
                event = e
                break
        return event