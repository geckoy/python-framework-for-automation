from events.BaseListener import BaseListener

class app_closed(BaseListener):
    
    def run(self):
        self.app.run_services("app_closed")