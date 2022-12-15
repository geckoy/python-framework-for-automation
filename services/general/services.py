from App.Helpers import *
from services.general.BaseService import BaseService
from services.general.service import service
class services:
    """
    ### Explanation:
    this class meant to be the service manager for each service
    ### Args :
    accept no args.
    """
    def __init__(self) -> None:
        self.app = getApplication(True)
        if not self.app: raise Exception(f"No Application has been detected in {__file__}")
        self.services = []
        self.initilize()
        self.app.run_services = self.run_services     
        self.app.services = self

    def initilize(self) -> None:
        """
        ### Explanation:
        This method get executed when app is registered in service manager and also services bag is created
        ### Args:
        accept no args.
        ### return:
        None
        """
        debugMsg("Loading Services ...")
        ServicesfilePath = "services/service"
        filesNames = [ f.replace(".py", "") for f in os.listdir(ServicesfilePath) if not re.match('__.*__', f)]
        idCounter = 0
        for n in filesNames:
            idCounter+=1
            filePath = (ServicesfilePath.replace("/",".") + (("." + n)))
            m = importlib.import_module(filePath)
            cls = getattr(m, n)
            if issubclass(cls, BaseService):
                self.add_service(service(idCounter, n, cls, filePath, True, self.app))
                debugMsg("loaded Service : {}", filePath)
    
    def run_services(self, event) -> None:
        """
        ### Explanation:
        This is the entry point for every event launched by events class which run specific event for specific service listeners
        ### Args:
        @event: string [ any event inside the listeners of events/listeners], this sepcify which event been executed and called the service, required.
        ### return:
        None
        """
        services = self.get_services()
        for s in services:
            s.run(event)

    def add_service(self, serviceObj) -> None:
        """
        ### Explanation:
        this method add service to the services bag
        ### Args:
        @serviceObj: object, the single service managing class, required. 
        """
        self.services.append(serviceObj)
    
    def get_services(self) -> list[service]:
        """
        ### Explanation:
        this method return all of the service managing classes
        ### Args:
        accept no args.
        ### return:
        list, containing the service managing object.
        """
        return self.services