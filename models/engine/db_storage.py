#!/usr/bin/python3
""" Engine Database """
from models.base_model import BaseModel
from models.base_model import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from os import getenv
from models.state import State
from models.city import City
from models.user import User
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class DBStorage:
    """Class Storage"""
    __engine = None
    __session = None

    def __init__(self):
        """Instance a DBStorage object"""
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(HBNB_MYSQL_USER,
                                              HBNB_MYSQL_PWD,
                                              HBNB_MYSQL_HOST,
                                              HBNB_MYSQL_DB),
                                      pool_pre_ping=True)
        if HBNB_ENV == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ query on the current database session (self.__session)
        all objects depending of the class name (argument cls) """
        if cls is not None:
            if type(cls) == str:
                cls = eval(cls)
            new_query = self.__session.query(cls)
        else:
            new_query = self.__session.query(State).all()
            new_query.extend(self.__session.query(City).all())
            new_query.extend(self.__session.query(User).all())
            new_query.extend(self.__session.query(Place).all())
            new_query.extend(self.__session.query(Review).all())
            new_query.extend(self.__session.query(Amenity).all())
        obj_dic = {}
        for ob in new_query:
            keys = "{}.{}".format(type(ob).__name__, ob.id)
            obj_dic[keys] = ob
        return obj_dic

    def new(self, obj):
        """ Add the object to the current database session """
        self.__session.add(obj)

    def save(self):
        """ Commit all changes of the current database session """
        self.__session.commit()

    def delete(self, obj=None):
        """ Delete from the current database session obj if not None """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """ create all tables in the database (feature of SQLAlchemy) """
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(sessionmaker(bind=self.__engine,
                                              expire_on_commit=False))
        self.__session = Session()

    def close(self):
        """ close session """
        self.__session.close()
