from events.BaseListener import BaseListener

class app_loop_process(BaseListener):
    def run(self):
        self.app.run_services("app_loop_process")