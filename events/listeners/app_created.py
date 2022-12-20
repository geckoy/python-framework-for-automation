from events.BaseListener import BaseListener
from services.general.servicesManager import servicesManager
class app_created(BaseListener):
    """
    Here where you register your abstract concept of process_management and other class instantiation.
    """
    def run(self):
        servicesManager() 