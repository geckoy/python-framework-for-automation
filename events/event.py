
class event:
    """
    ### Explanation:
    This class manage the registered event 
    ### Args:
    @name: string, name of the service, required.
    @cls: object, real class of the event handler, required.
    @path: string, path of the real class event handler, required.
    @args: list, arguments that will be push into real class event paranthesis, optional.
    ### return:
    None
    """
    def __init__(self, name:str, cls, path:str, *args) -> None:
        self.e_class = cls(*args)
        self.e_name = name
        self.e_path = path

    def run(self, *args):
        """
        ### Explanation:
        method execute the event when launched in interval way
        ### Args:
        accept no args.
        ### return:
        None
        """
        self.e_class.run(*args)