from App.Helpers import *
from services.general.BaseService import BaseService
from services.general.service import service
from App.abstract.process_managment.BaseProcesses import BaseProcesses
class services(BaseProcesses):
    """
    ### Explanation:
    this class meant to be the service manager for each service
    ### Args :
    accept no args.
    """
    processname = "service"
    processespath = "services/service"
    processesManagerPath = "services/general/service"
    
    def __init__(self) -> None:
        super().__init__()
        self.app.services = self
        self.app.run_services = self.run_services

    def run_services(self, event) -> None:
        """
        ### Explanation:
        This is the entry point for every event launched by events class which run specific event for specific service listeners
        ### Args:
        @event: string [ any event inside the listeners of events/listeners], this sepcify which event been executed and called the service, required.
        ### return:
        None
        """
        self.run_processes(event)

        
    def get_services(self) -> list[service]:
        """
        ### Explanation:
        this method return all of the service managing classes
        ### Args:
        accept no args.
        ### return:
        list, containing the service managing object.
        """
        return self.get_processes()
    
    def get_service(self, name:str) -> service|None:
        """
        ### Explanation:
        this method return the service managing class according to the provided name.
        ### Args:
        @name: string, name of the wanted service to retreive, required.
        ### return:
        object, containing the service managing object.
        None, if the service not found.
        """
        return self.get_process(name)