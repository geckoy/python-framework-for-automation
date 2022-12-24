from commands.BaseCommand import BaseCommand
from App.Helpers import *
from App.abstract.process_managment.BaseProcessCommands import BaseProcessCommands
class vpsampleCommands(BaseCommand, BaseProcessCommands):

    processname = "vpsample"

    def exec(self, action: str, metaData: dict) -> exec_command_returned_dict:
        return super().execAbstract(action, metaData)