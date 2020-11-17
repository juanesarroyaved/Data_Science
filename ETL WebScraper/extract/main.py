import argparse #librería estándar de python
import csv #librería para trabajar con archivos csv
import datetime #librería de fechas
import logging #librería para mostrar info mientras la ejecución del código
logging.basicConfig(level=logging.INFO) #serán mensajes informativos
import re #librería para Expresiones Regulares

from requests.exceptions import HTTPError, ConnectionError #importamos los errores de requests
from urllib3.exceptions import MaxRetryError #importamos los errores de urllib3

import news_page_objects as news #importamos la info del archivo news_page_objects
from common import config #importamos de common.py la configuración


logger = logging.getLogger(__name__) #una referencia a nuestro logger
#Nuestro link empieza con HTTP, la S es opcional (?), por lo menos uno o más letras (.+)
#Luego va un (/), luego una letra o más (.+) y luego terminamos el patrón ($)
is_well_formed_link = re.compile(r'^https?://.+/.+$') #https://example.com/hello <- este patrón haría match
#Si es un link basado en la raíz
#Empieza (^) con un slash (/), tiene una o más letras (.+) y terminamos el patrón ($)
is_root_path = re.compile(r'^/.+$') # /some-text <-- este haría match


def _news_scraper(news_site_uid):
    host = config()['news_sites'][news_site_uid]['url'] #obtenemos el host, y obtenemos la url (de yaml) del sitio que el usuario seleccionó

    logging.info('Beginning scraper for {}'.format(host)) #mostrará que se está iniciando el scrapeo
    homepage = news.HomePage(news_site_uid, host) #nuestro homepage es el objeto HomePage del modulo news que importamos de otro archivo

    articles = []
    for link in homepage.article_links: #por c/link en homepage
        article = _fetch_article(news_site_uid, host, link)

        if article: #si article no está vacío
            logger.info('Article fetched!!')
            articles.append(article) #añade el articulo

    _save_articles(news_site_uid, articles) #guardamos esto en un archivo


def _save_articles(news_site_uid, articles): # funcion para guardar la info en un archivo
    now = datetime.datetime.now().strftime('%Y_%m_%d') #obtiene la fecha de hoy con la funcion .now() en un formato especificado con la funcion .strftime()
    out_file_name = '{news_site_uid}_{datetime}_articles.csv'.format(
        news_site_uid=news_site_uid,
        datetime=now) #definimos el nombre del archivo
    #generamos los encabezados en forma de lista
    #lambda es una función inline
    csv_headers = list(filter(lambda property: not property.startswith('_'), #que no comiencen con '_'
                        dir(articles[0]))) #escogemos el primer articulo
    
    with open(out_file_name, mode='w+') as f: #abrimos archivo en modoe escritura ('w+') el + lo crea en caso que no exista
        writer = csv.writer(f) #writer de csv
        writer.writerow(csv_headers) #escriba la primera fila con los encabezados

        for article in articles: #por cada artículo
            #obtiene cada atributo de cada articulo dentro de csv_headers, cada atributo lo obtuvimos con dir(articles[0])
            row = [str(getattr(article, prop)) for prop in csv_headers] #getattr obtiene los atributos
            writer.writerow(row) #escribe una nueva fila con la vble row, también como lista


def _fetch_article(news_site_uid, host, link):
    logger.info('Start fetching article at {}'.format(link)) #mensaje

    article = None #inicializamos vacío la variable
    try: #ErrorHandler: errores en solicitudes a la web
        article = news.ArticlePage(news_site_uid, _build_link(host, link)) #el vinculo los contruimos con la funcion _buil_linl()
    except (HTTPError, ConnectionError, MaxRetryError) as e: #atrapamos lo errores que queremos: HTTPError, ConnectionError y MaxRetryError
        logger.warning('Error while fechting the article', exc_info=False) #le daré esta información al usuario y que no me muestre el error en la consola


    if article and not article.body: #Si tenemos un article y el articulo no tiene body
        logger.warning('Invalid article. There is no body') #no hay nada aquí
        return None

    return article


def _build_link(host, link):
    if is_well_formed_link.match(link): #será verdadero si tenemos un match
        return link #regresamos el link
    elif is_root_path.match(link): #si está basado en la raíz
        return '{}{}'.format(host, link) #construimos el vinculo con el host y el link
    else: #no hizo match con ninguna
        return '{host}/{uri}'.format(host=host, uri=link) #lo construimos con host y uri


if __name__ == '__main__': #entry point
    parser = argparse.ArgumentParser() #inicializamos un parser con un parseador de arfgumentos

    news_site_choices = list(config()['news_sites'].keys()) #las opciones son la primera llave de config y aplicamos el método keys, todo esto convertido a lista
    parser.add_argument('news_site', #añadimos un argumento llamado news_site
                        help='The news site that you want to scrape', #una ayuda para el argumento
                        type=str, #de tipo cadena
                        choices=news_site_choices) #opciones de elección

    args = parser.parse_args() #parsea los argumentos
    _news_scraper(args.news_site) #argumento será el news_site
     