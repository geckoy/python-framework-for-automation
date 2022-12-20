from events.BaseListener import BaseListener

class app_closed(BaseListener):
    
    def run(self):
        self.app.events.accept_all_events("app_closed")