import argparse #parsear argumentos del usuario
import logging #mensajes informativos
logging.basicConfig(level=logging.INFO) #mensajes de nivel INFO

import pandas as pd #para leer los csv

from article import Article #importamos del archivo article.py la clase Article
from base import Base, engine, Session #del archivo base.py importa engine, Session y Base


logger = logging.getLogger(__name__)


def main(filename):
    Base.metadata.create_all(engine) #configuramos el ambiente de sqlalchemy. Generar nuestro schema de la DB
    session = Session() #Inicializar nuestra sesión
    articles = pd.read_csv(filename) #reemos el csv
    #.iterrows() genera un loop dentro de cada una de nuestras filas. Nos entrega el indice y la columna
    for index, row in articles.iterrows():
        logger.info('Loading article id {} into DB'.format(row['uid']))
        article = Article(row['uid'], #pasamos cada uno de nuestros valores al constructor.
                          row['body'],
                          row['host'],
                          row['newspaper_uid'],
                          row['n_tokens_body'],
                          row['n_tokens_title'],
                          row['title'],
                          row['url'])
        session.add(article) #nos mete nuestro articulo en la BD

    session.commit() #commit a la sesión
    session.close() #tenemos que cerrarla


if __name__ == '__main__':
    parser = argparse.ArgumentParser() #parseador de argumentos
    parser.add_argument('filename', #añadimos argumento filename
                        help='The file you want to load into the db', #ayuda del argumento
                        type=str) #cadena de texto

    args = parser.parse_args() #parsea los argumentos

    main(args.filename)

    engine, metadata logger

