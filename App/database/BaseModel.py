from App.Helpers import *
from peewee import Model

class BaseModel(Model):
    
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.debug = kwargs.get("debug", False)
        self.db = getDatabaseConnection(debug=self.debug)
        
    def __getattribute__(self,name):
        attr = object.__getattribute__(self, name)
        if hasattr(attr, '__call__') and re.match("^model", name):
            def newfunc(*args, **kwargs):
                self.connect()
                debugMsg("Connection to db successful", Force=self.debug)
                result = attr(*args, **kwargs)
                self.close()
                debugMsg("Connection to db closed", Force=self.debug)
                return result
            return newfunc
        else:
            return attr

    def connect(self):
        self.db.connect(True)

    def close(self):
        self.db.close()

    @classmethod
    def inheritors_classes(klass) -> list:
        """
        This method return the classes that inherit the BaseModel class.
        """
        for d in listdir():
            if re.match(".*Process", d, re.IGNORECASE):
                processname = d.replace("Process", "")
                path = f"{processname}Process.general.models"
                importlib.import_module(path)
        importlib.import_module("App.database.models")
        subclasses = []
        work = [klass]
        while work:
            parent = work.pop()
            for child in parent.__subclasses__():
                if child not in subclasses:
                    subclasses.append(child)
                    work.append(child)
        return subclasses
    
    class Meta:
        database = getEnvDB()
