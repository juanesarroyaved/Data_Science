# -*- coding: utf-8 -*-

import argparse
import csv
import datetime
import logging
logging.basicConfig(level=logging.INFO)
import re #re significa Expresiones Regulares

from requests.exceptions import HTTPError
from urllib3.exceptions import MaxRetryError

import news_page_objects as news
from common import config #importo la vble global _config del archivo common.py

logger = logging.getLogger(__name__)

#utilizaremos expresiones regulares para definir que tipo de link encontramos.
is_well_formed_link = re.compile(r'^https?://.+/.+$') #r: es un string raw. ^: marca el inicio de la palabra. s?: la s es opcional. .+: por lo menos uno o más letras. $: terminamos el patrón.  
#para identificar que patrón haría match y sería un link bien formado. Match: https://elpais.com/no
is_root_path = re.compile(r'^/.+$') #match: /some-text

def _news_scraper(news_site_uid):
	host = config()['news_sites'][news_site_uid]['url']

	logging.info('Beginning scraper for {}'.format(host))
	homepage = news.HomePage(news_site_uid, host)

	articles=[]
	for link in homepage.article_links:
		article = _fetch_article(news_site_uid, host, link)

		if article:
			logger.info('Article fetched!!!')
			articles.append(article)
			print(article.title)

	_save_articles(news_site_uid, articles)

def _save_articles(news_site_uid, articles):
	now = datetime.datetime.now().strftime('%Y_%m_%d')
	out_file_name = '{news_site_uid}_{datetime}_articles.csv'.format(news_site_uid=news_site_uid, datetime=now)
	csv_headers = list(filter(lambda property: not property.startswith('_'), dir(articles[0])))

	with open(out_file_name, mode='w+') as f:
		writer = csv.writer(f)
		writer.writerow(csv_headers)

		for article in articles:
			row = [str(getattr(article, prop)) for prop in csv_headers]
			writer.writerow(row)


def _fetch_article(news_site_uid, host, link):
	logger.info('Start fetching article at {}'.format(link))

	article = None
	try: #error handler para hacer mi código más robusto. Ante solicitudes http me puedo encontrar muchos errores.
		article = news.ArticlePage(news_site_uid, _build_link(host,link))
	except (HTTPError, MaxRetryError) as e:
		logger.warning('Error while fetching the article', exc_info=False)
		
	if article and not article.body:
		logger.warning('Invalid article. There is no body')
		return None
	else:
		return article

def _build_link(host, link):
	if is_well_formed_link.match(link):
		return link
	elif is_root_path.match(link):
		print('{}{}'.format(host,link))
		return '{}{}'.format(host,link)
	else:
		print('{host}/{uri}'.format(host=host, uri=link))
		return '{host}/{uri}'.format(host=host, uri=link)


if __name__ == '__main__':
	parser = argparse.ArgumentParser() #parseador de argumentos

	news_site_choices = list(config()['news_sites'].keys()) #enlista las opciones de sitios que definimos en el archivo yaml
	parser.add_argument('news_site', help='The news site that you want to scrape', type=str, choices=news_site_choices) #agrega un argumento según las opciones de sitios

	args = parser.parse_args()
	_news_scraper(args.news_site)