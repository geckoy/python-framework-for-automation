
class service:
    """
    ### Explanation:
    This class is service managing class which stop pause start the services
    ### Args:
    @id: int, service identification, required.
    @name:string, name of the services, required.
    @cls:class, the real service class, required.
    @path: string, path of the real service class, required.
    @autoStart:bool, if auto launch at starting, required.
    @args: list, argument that will be passed to the real service class at instantiation, default: empty list.
    ### return:
    None
    """
    def __init__(self, id:int, name:str, cls, path:str, autoStart:bool, *args) -> None:
        self.id = id
        self.name = name
        self.service_class = cls
        self.service_path = path
        self.autoStart = autoStart
        self.service_args = args
        self.service_obj = None
        self.initilize()

    def initilize(self) -> None:
        """
        ### Explanation:
        executed after the service manager has registered everything.
        ### Args:
        accept no args
        ### return:
        None
        """
        if self.autoStart:
            self.start()

    def run(self, event) -> None:
        """
        ### Explanation:
        this method meant to execute the service in interval way.
        ### Args:
        @event: string [ any event inside the listeners of events/listeners], this sepcify which event been executed and called the service, required.
        ### return:
        None
        """
        if self.service_obj != None and not hasattr(self.service_obj, "parallel") and hasattr(self.service_obj, "events"):
            if event in self.service_obj.events:
                self.service_obj.run(event)
    
    def start(self):
        """
        ### Explanation:
        init the service
        ### Args:
        accept no args.
        ### return:
        None
        """
        self.service_obj = self.service_class(*self.service_args)
    
    def stop(self):
        """
        ### Explanation:
        destroy the service memory allocation "destruct the object"
        ### Args:
        accept no args.
        ### return:
        None
        """
        del self.service_obj
        self.service_obj = None