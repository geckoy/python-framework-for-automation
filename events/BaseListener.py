from abc import ABC, abstractmethod
class BaseListener(ABC):
    def __init__(self, application) -> None:
        self.app = application
    
    @abstractmethod
    def run(self):
        """
        ### Explanation:
        method execute the event when launched in interval way
        ### Args:
        accept no args.
        ### return:
        None
        """
        pass