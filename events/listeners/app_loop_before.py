from events.BaseListener import BaseListener

class app_loop_before(BaseListener):
    def run(self):
        self.app.run_services("app_loop_before")