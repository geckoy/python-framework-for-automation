from events.BaseListener import BaseListener
from services.general.services import services
class app_starting(BaseListener):
    def run(self):
        self.app.run_services("app_starting")