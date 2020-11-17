from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base #tener acceso a funcionalidades de Object Relational Manager
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///newspaper.db') #Nuestro motor. Quiero usar sqlite

Session = sessionmaker(bind=engine) #Generar objeto session y le pasamos nuestro motor

Base = declarative_base() #Nuestra calse base