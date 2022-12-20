from abc import ABC, abstractmethod


class BaseProcess(ABC):
    """
    ### Explanation:
    This abstract class is used with each process want to integrate it in app BaseMultiProcessing
    ### Args:
    @appli: object application, the main application, required.
    ### return:
    None
    """
    def __init__(self) -> None:
        self.initilize()
        
    @property
    def events(self)-> list[str]:
        """
        which events the process is listening to, this typehint is added forcebly so don't try to check it with hasattr().
        """
        pass

    @abstractmethod
    def initilize(self) -> None:
        """
        This method is executed when class is created don't try to fetch data from other processes that inherit process_management abstract concept.
        """
        pass

    @abstractmethod
    def run(self, event:str) -> None:
        """
        ### Explanation:
        this method meant to execute the service in interval way.
        ### Args:
        @event: string [ any event inside the listeners of events/listeners], this sepcify which event been executed and called the service, required.
        ### return:
        None
        """
        pass
    
    @abstractmethod
    def app_close(self):
        """
        ### Explanation:
        abstarct magic method executed when removing object from mem
        """
        pass

#* State the Problems clearly:
#===============================
#  we need a base service application and it will connect each service to some specific app event in eventsApi. 
# #
#* try to cover All eadge cases:
#=================================
#  4. can access db
#  6. each service has the ability to work in parallel or sync
#
#* Done:
#=======
#  1. each service is added to service folder and the services.py will read all the services inside directory auto and also instantiate them  
#  2. each has the ability to listen for some event of app.
#  3. can access the app.
#  5. having a class that connect them all using services.py
# #