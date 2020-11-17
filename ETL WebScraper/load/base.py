from sqlalchemy import create_engine #librería para sql y crear un engine (motor)
from sqlalchemy.ext.declarative import declarative_base #acceso a funcionalidades de ORM (Object Relational Mapper) de sqlalchemy
#para trabajar con objetos de Python en vez de consultas propias de SQL
from sqlalchemy.orm import sessionmaker #Creador de sesiones

engine = create_engine('sqlite:///newspapers.db') #creamos nuestro motor. Queremos usar sqlite y creamos la DB newspaper.db

Session = sessionmaker(bind=engine) #creamos la sesión con el motoro engine

Base = declarative_base() #generamos nuestra clase base para extender los modelos

