import requests
import bs4

from common import config #nos da acceso a la función condig y a manipular la configuración

class NewsPage:

	def __init__(self, news_site_uid, url):
		self._config = config()['news_sites'][news_site_uid] 
		self._queries = self._config['queries'] #obtener queries de esta configuración
		self._html = None #la inicializo sin valor

		self._visit(url)

	def _select(self, query_string):
		return self._html.select(query_string)

	def _visit(self,url): #con esto voy a visitar directamente el sitio web
		response = requests.get(url)

		response.raise_for_status() #este método nos permite saber si la solicitud tuvo un error

		self._html = bs4.BeautifulSoup(response.text, 'html.parser')

class HomePage(NewsPage): #representa la página ppal de nuestra web. Lo convierto en una subclase de NewsPage.

	def __init__(self, news_site_uid, url): #método para inicializar y que recibe el id del sitio y la url
		super().__init__(news_site_uid,url) #la función super() nos da acceso al metodo __init__

	@property
	def article_links(self):
		link_list = []
		for link in self._select(self._queries['homepage_article_links']):
			if link and link.has_attr('href'):
				link_list.append(link)

		return set(link['href'] for link in link_list)

class ArticlePage(NewsPage):
	def __init__(self, news_site_uid, url):
		super().__init__(news_site_uid,url)

	@property
	def body(self):
		result = self._select(self._queries['article_body'])
		return result[0].text if len(result) else ''

	@property
	def title(self):
		result = self._select(self._queries['article_title'])
		return result[0].text if len(result) else ''
	