# -*- coding: utf-8 -*-

import argparse #nos permite manejar argumentos dados por el usuario al momento de ejecución del código
import pandas as pd

from article import Article #importo desde otros archivos cualquier tipo de objeto: vbles, clases...
from base import Base, engine, Session

def main(filename):
	Base.metadata.create_all(engine)
	session = Session()
	articles = pd.read_csv(filename)

	articles.drop_duplicates(subset=['ID de candidato'], keep= 'first', inplace= True)

	for index, row in articles.iterrows():
		article = Article(row['ID de candidato'],
						row['ID de solicitud de puesto'],
						row['Género'])

		session.add(article)

	session.commit()
	session.close()

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('filename', help='The file you wanna upload into db.', type=str)
	args = parser.parse_args()

	filename = 'Candidatos_Conectados.csv'

	main(args.filename)
