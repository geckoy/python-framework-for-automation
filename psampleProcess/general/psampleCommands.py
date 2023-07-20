from commands.BaseCommand import BaseCommand
from App.Helpers import *
from App.abstract.process_managment.BaseProcessCommands import BaseProcessCommands
class psampleCommands(BaseCommand, BaseProcessCommands):

    processname = "psample"
    
    def initilize(self) -> None:
        pass

    def exec(self, action: str, metaData: dict) -> exec_command_returned_dict:
        return super().execAbstract(action, metaData)