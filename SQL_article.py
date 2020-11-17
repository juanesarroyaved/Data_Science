from sqlalchemy import Column, String, Integer

from base import Base

class Article(Base):
	__tablename__ = 'articles'

	id = Column(Integer, primary_key=True)
	id_req = Column(Integer)
	gender = Column(String)

	def __init__(self,
				id_candidato,
				id_requisicion,
				gender):#generar nuestra inicialización del objeto
		self.id = id_candidato
		self.id_req = id_requisicion
		self.gender = gender