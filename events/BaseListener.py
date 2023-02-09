from abc import ABC, abstractmethod
class BaseListener(ABC):
    def __init__(self, appli) -> None:
        from app import application
        self.app : application = appli
    
    @abstractmethod
    def run(self, *args):
        """
        ### Explanation:
        method execute the event when launched in interval way
        ### Args:
        accept no args.
        ### return:
        None
        """
        pass