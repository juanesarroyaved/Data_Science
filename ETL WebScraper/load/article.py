from sqlalchemy import Column, String, Integer #importamos los tipos de datos de sqlalchemy (str, col, int)

from base import Base #importa de base.py nuestra clase Base


class Article(Base): #Articulo extiene Base
    __tablename__ = 'articles' #como se va a llamar nuestra tabla

    id = Column(String, primary_key=True) #definimos id como la clave de la tabla y es String
    body = Column(String)
    host = Column(String)
    title = Column(String)
    newspaper_uid = Column(String)
    n_tokens_body = Column(Integer)
    n_tokens_title = Column(Integer)
    url = Column(String, unique=True) #tiene que tener valores únicos (unique=True)

    #método para inicializar la clase/objeto
    def __init__(self, uid, body, host, newspaper_uid, n_tokens_body, n_tokens_title, title, url):
        #lo asignamos a nuestras variables de instancia
        self.id = uid
        self.body = body
        self.host = host
        self.title = title
        self.newspaper_uid = newspaper_uid
        self.n_tokens_body = n_tokens_body
        self.n_tokens_title = n_tokens_title
        self.url = url

