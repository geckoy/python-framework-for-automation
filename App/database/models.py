from peewee import CharField
from App.database.BaseModel import BaseModel


class Settings(BaseModel):
    name = CharField()
    name_value = CharField()
    
    @classmethod
    def modelCreate(cls, **kwargs):
        obj = cls.create(**kwargs)