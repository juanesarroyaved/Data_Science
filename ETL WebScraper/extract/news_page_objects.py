import bs4 #librería para parsear códigos: HTML, XML...
import requests #librería para hacer solicitudes a la web

from common import config #importamos la funcion config del modulo (archivo) common.py

class NewsPage:

    def __init__(self, news_site_uid, url):
        self._config = config()['news_sites'][news_site_uid] #una ref a nuestra config, accedemos a la primera llave, le pasamos el id del sitio como parametro del usuario
        self._queries = self._config['queries'] #queremos los queries que se encuentran en nuestra configuracion
        self._html = None #inicializamos una variable sin valor
        self._url = url

        self._visit(self._url) #visitamos el sitio con la url

    def _select(self, query_string): #obtener info del documento que acabamos de parsear
        return self._html.select(query_string) #seleccionar el query

    def _visit(self, url): #visitar directamente el sitio web
        response = requests.get(url) #solicitud para obtener el cod HTML del sitio

        response.raise_for_status() #nos permite aventar un error si la solicitud no se completó correctamente

        self._html = bs4.BeautifulSoup(response.text, 'html.parser') #parseamos el codigo html con bs4

#Homepage se vuelve un hijo de NewsPage. HomePage extiende NewsPage
class HomePage(NewsPage): #Representará la pag ppal de nuestra web

    def __init__(self, news_site_uid, url): #recibe el id del sitio de noticias y una url
        super().__init__(news_site_uid, url) #funcion para poder inicializar esta superclase y que nos da acceso al método __init__

    @property #generamos nuestra primer propiedad
    def article_links(self): #links, lo que nos interesa de la HomePage
        link_list = [] #inicializamos lista vacía
        for link in self._select(self._queries['homepage_article_links']): #por cada link de los queries
            if link and link.has_attr('href'): #si se tiene un link y el link tiene el atributo [href] 
                link_list.append(link) #se añade en la lista de links

        return set(link['href'] for link in link_list) #garantiza que no tenemos elementos repetidos porque un set no permite valores duplicados


class ArticlePage(NewsPage): #Extiende NewsPage (es un tipo de página de noticia)

    def __init__(self, news_site_uid, url):
        super().__init__(news_site_uid, url) #método super para inicializar la superclase

    @property
    def body(self): #declaramos la propiedad body
        result = self._select(self._queries['article_body']) #queremos el query article_body de config.yaml
        #podemos usar select porque ArticlePage es una extensión de NewsPage (donde está el método select)
        return result[0].text if len(result) else '' #regresaré el primer elemento de la lista con su texto. Si está vacío no regresa nada

    @property
    def title(self): #declaramos la propiedad título de la calse ArticlePage
        result = self._select(self._queries['article_title']) #query article_title
        return result[0].text if len(result) else '' #retorna el primer elemento

    @property
    def url(self): #definimos propiedad url
        return self._url

