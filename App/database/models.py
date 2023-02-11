from peewee import CharField
from App.database.BaseModel import BaseModel


class Settings(BaseModel):
    name = CharField()
    name_value = CharField()
    
    def modelCreate(self, **kwargs):
        obj = self.create(**kwargs)