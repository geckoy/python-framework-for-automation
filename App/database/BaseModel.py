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

    class Meta:
        database = getDatabaseConnection() # This model uses the "people.db" database.
