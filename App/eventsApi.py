from App.Helpers import *

class events:
    def __init__(self, appli) -> None:
        from app import application
        self.application :application = appli

    def app_created(self) -> None:
        """
        ### Explanation:
        this event is launched when application is registered in memory and all running good. better to put inside all intilization stuff 'abstract stuff from app because isn't fully loaded only push don't try to fetch stuff from app or other classes'.
        ### return:
        None
        """
        debugMsg("Application created event launched")
        self.application.exec_event("app_created", memory().get("specific_processes", ""))
        debugMsg("Application created event ended")

    def app_loop_before(self) -> None:
        """
        ### Explanation:
        this event is launched before running the loop process. "runs on every iteration"
        ### return:
        None
        """
        self.application.exec_event("app_loop_before")


    def app_loop_process(self) -> None:
        """
        ### Explanation:
        this event is launched when running the loop process. "runs on every iteration"
        ### return:
        None
        """
        self.application.exec_event("app_loop_process")

    def app_loop_after(self) -> None:
        """
        ### Explanation:
        this event is launched after running the loop process. "runs on every iteration"
        ### return:
        None
        """
        self.application.exec_event("app_loop_after")


    def app_closed(self) -> None:
        """
        ### Explanation:
        this event is launched when application is closing.
        ### return:
        None
        """
        print(f"Application Closing ...")
        try:
            self.application.exec_event("app_closed")
        except BaseException as err:
            print("'app_closed' catched an error : {}".format(err))

        