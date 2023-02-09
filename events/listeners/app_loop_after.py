from events.BaseListener import BaseListener

class app_loop_after(BaseListener):
    def run(self, *args):
        self.app.events.accept_all_events("app_loop_after")