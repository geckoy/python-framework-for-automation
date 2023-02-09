from events.BaseListener import BaseListener

class app_loop_before(BaseListener):
    def run(self, *args):
        self.app.events.accept_all_events("app_loop_before")