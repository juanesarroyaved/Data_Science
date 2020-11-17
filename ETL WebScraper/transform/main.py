# -*- coding: utf-8 -*-

import argparse #librería para argumentos
import hashlib #librería estandar de python. Para operaciones criptográficas. para generar hash de la url
import logging #librería para mensajes informativos
logging.basicConfig(level=logging.INFO) #mensajes a nivel informativo
from urllib.parse import urlparse #parseador de urllib


import pandas as pd #transformacion de datos
#Natural Language Tokenizer
import nltk #Librería del stack de data science de python.
from nltk.corpus import stopwords #stopwords son palabras que no añaden ningún tipo de valor

logger = logging.getLogger(__name__) #__name__ nombre interno de nuestro archivo

def main(filename):
    logger.info('Starting cleaning process') #iniciando el proceso

    df = _read_data(filename) #funcion para leer los datos
    newspaper_uid = _extract_newspaper_uid(filename) #extraer el uid del newspaper
    df = _add_newspaper_uid_column(df, newspaper_uid) #añade columna al dataframe con el newspaper_uid
    df = _extract_host(df) #extrae el host de las url's
    df = _fill_missing_titles(df) #llena valores faltantes
    df = _generate_uids_for_rows(df) #asigna un uid o código hexadecimal único para cada fila.
    df = _remove_new_lines_from_body(df) #eliminar saltos de línea en el body del articulo
    df = _tokenize_column(df, 'title') #enriquecimiento de los datos con nltk: columna title
    df = _tokenize_column(df, 'body') #enriquecimiento de los datos con nltk: columna body
    df = _remove_duplicate_entries(df, 'title') #eliminamos duplicados
    df = _drop_rows_with_missing_values(df) #eliminamos columnas con valores faltantes
    _save_data(df, filename) #guarda los datos en un csv

    return df


def _read_data(filename):
    logger.info('Reading file {}'.format(filename))

    return pd.read_csv(filename) #lector de archivos csv de Pandas

def _extract_newspaper_uid(filename):
    logger.info('Extracting newspaper uid')
    newspaper_uid = filename.split('_')[0] #separa valores por '_' y toma el primer elemento (newspaper_uid)

    logger.info('Newspaper uid detected: {}'.format(newspaper_uid))
    return newspaper_uid

def _add_newspaper_uid_column(df, newspaper_uid):
    logger.info('Filling newspaper_uid column with {}'.format(newspaper_uid))
    df['newspaper_uid'] = newspaper_uid #crea una columna al df donde todos los valores serán el newspaper_uid

    return df

def _extract_host(df):
    logger.info('Extracting host from urls')
    df['host'] = df['url'].apply(lambda url: urlparse(url).netloc) #crea una columna 'host' con el valor de la url
    # la url la obtiene con la función inline (lambda: a cada línea del df) de urlparse(url).netloc

    return df

def _fill_missing_titles(df):
    logger.info('Filling missing titles')
    missing_titles_mask = df['title'].isna() #obtiene en una vble como df los valores NA

    missing_titles = (df[missing_titles_mask]['url'] #la columna url del df con valores faltantes (df[na])
                        .str.extract(r'(?P<missing_titles>[^/]+)$') #Queremos seleccionar todo MENOS los slash [^/]. extrae expresion regular dandole el nombre de 'missing titles'
                        .applymap(lambda title: title.split('-')) #mapa: función inline donde separa por '-'
                        .applymap(lambda title_word_list: ' '.join(title_word_list)) #mapa: juntar la lista del paso anterior
                      )

    #lo asignamos a la columna 'title' donde hay valores NA's. Le pasamos el grupo de la Exp. Regular.
    df.loc[missing_titles_mask, 'title'] = missing_titles.loc[:, 'missing_titles']

    return df

def _generate_uids_for_rows(df):
    logger.info('Generating uids for each row')
    uids = (df
            .apply(lambda row: hashlib.md5(bytes(row['url'].encode())), axis=1) # Esto nos da un número de 128 bits.axis=1 para FILAS. axis=0 sería COLUMNAS
            .apply(lambda hash_object: hash_object.hexdigest()) #que nos dé su representación hexadecimal
            )

    df['uid'] = uids #se lo añadimos a una columna

    return df.set_index('uid') #definimos que la nueva columna 'uid' es nuestro índice

def _remove_new_lines_from_body(df):
    logger.info('Remove new lines from body')

    stripped_body = (df #seleccionamos nuestro df
                     .apply(lambda row: row['body'], axis=1) #una modif a c/row con axis=1
                     .apply(lambda body: list(body)) #lo convertimos en una lista de letras
                     .apply(lambda letters: list(map(lambda letter: letter.replace('\n', ' '), letters))) #reemplaza los saltos de carro (/n) por espacios ' '. el 2do parametro de maps es la lista que trabajará (letters)
                     .apply(lambda letters: ''.join(letters)) #une la lista en un string
                    )

    df['body'] = stripped_body #asigna los nuevos cuerpos a la columna body

    return df

def _tokenize_column(df, column_name): #tokenizar el titulo y el body
    logger.info('Calculating the number of unique tokens in {}'.format(column_name))
    stop_words = set(stopwords.words('spanish')) #definir stopwords en español dentro de un set.
    #esto me agrega en un set todas las palabras que no me añaden ningún valor

    n_tokens =  (df
                 .dropna() #eliminamos los nulos porque nltk fallaría
                 .apply(lambda row: nltk.word_tokenize(row[column_name]), axis=1) #tokeniza la fila con la columna (title, body)
                 .apply(lambda tokens: list(filter(lambda token: token.isalpha(), tokens))) #filtramos unicamente palabras alphanumericas. Convertimos en lista porque nos devuelve un iterador
                 .apply(lambda tokens: list(map(lambda token: token.lower(), tokens))) #convertir todos los tokens en minúsculas para compararlas con stopwords (todas en minusculas)
                 .apply(lambda word_list: list(filter(lambda word: word not in stop_words, word_list))) #filtramos palabras que no estén en las stop_words
                 .apply(lambda valid_word_list: len(valid_word_list)) #queremos la longitud de palabras valiosas o validas
            )

    df['n_tokens_' + column_name] = n_tokens #creamos la columna de tokens con los numeros de tokens para title y body

    return df

def _remove_duplicate_entries(df, column_name):
    logger.info('Removing duplicate entries')
    #Elimina duplicados con .drop_duplicates
    df.drop_duplicates(subset=[column_name], #la columna que no debe tener duplicados
                        keep='first', #que se quede con el primer valor
                        inplace=True) #reemplazarlo en el mismo df o guardarlo en otro?

    return df

def _drop_rows_with_missing_values(df):
    logger.info('Dropping rows with missing values')
    return df.dropna() #eliminamos las filas que no tienen valores

def _save_data(df, filename):
    clean_filename = 'clean_{}'.format(filename) #almacenamos el nombre del archivo
    logger.info('Saving data at location: {}'.format(clean_filename))
    df.to_csv(clean_filename) #guarda el df en un csv con el nombre previamente definido

if __name__ == '__main__':
    parser = argparse.ArgumentParser() #primero preguntaremos el archivo que queremos transformar
    parser.add_argument('filename', #añade argumento llamado filename
                        help='The path to the dirty data', #una ayuda para el argumento
                        type=str) #de tipo cadena de texto

    args = parser.parse_args() #parsear los argumentos

    df = main(args.filename) #funcion main con el argumento filename