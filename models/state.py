#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship('City', backref='State')

    if getenv('HBNB_TYPE_STORAGE') != 'db':
        @property
        def cities(self):
            """getter attribute cities that returns the list of
            City instances with state_id equals to the current State.id"""
            from models import storage
            from models.city import City
            new = []
            new_dic = storage.all(City)
            for k, v in new_dic.items():
                if v.state_id == self.id:
                    new.append(city)
            return new
