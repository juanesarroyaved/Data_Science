import logging #mensajes
logging.basicConfig(level=logging.INFO) #mensajes informativos
import subprocess #Librería std de Python: manipular directamente archivos de terminar


logger = logging.getLogger(__name__)
news_sites_uids = ['eluniversal', 'elpais'] #sitios de noticias


def main():
    #ejecuta las tres funciones de ETL: Extract, Transform y Load
    _extract()
    _transform()
    _load()


def _extract():
    logger.info('Starting extract process')
    for news_site_uid in news_sites_uids: #por cada sitio en news_sites_uids (eluniversal y el país)
        subprocess.run(['python', 'main.py', #escribe en la terminal 'python main.py'
                        news_site_uid], #le pasamos el argumento del sitio
                        cwd='./extract') #cwd=current workin directory. lo ejecutará en la sub-carpeta (./extract)
        #mover los archivos que se generaron con find y con mv
        subprocess.run(['find', '.','-name', '{}*'.format(news_site_uid), #encuentre algo con cierto patron (empieze con [news_site_uid]*) 
                        '-exec', 'mv', '{}', '../transform/{}_.csv'.format(news_site_uid), ';'], #mueve (mv) el archivo a la carpeta 'transform'
                       cwd='./extract') #que lo ejecute en la carpeta './extract'


def _transform():
    logger.info('Starting transform process')
    for news_site_uid in news_sites_uids: #por cada sitio en news_sites_uids (eluniversal y el país)
        dirty_data_filename = '{}_.csv'.format(news_site_uid) #define nombre de archivo
        clean_data_filename = 'clean_{}'.format(dirty_data_filename) #define nombre de archivo
        subprocess.run(['python', 'main.py', dirty_data_filename], #corre el script de transformar con el argumento del nombre del archivo
                        cwd='./transform') #que lo ejecute en la carpeta './transform'
        subprocess.run(['rm', dirty_data_filename], #que elimine los archivos sucios
                        cwd='./transform') #que lo ejecute en la carpeta './transform'
        subprocess.run(['mv', clean_data_filename, '../load/{}.csv'.format(news_site_uid)], #moverlo a la carpeta 'load'
                        cwd='./transform') #que lo ejecute en la carpeta './transform'


def _load():
    logger.info('Starting loading process')
    for news_site_uid in news_sites_uids: #por cada sitio en news_sites_uids (eluniversal y el país)
        clean_data_filename = '{}.csv'.format(news_site_uid) #define nombre del archivo
        subprocess.run(['python', 'main.py', clean_data_filename], #ejecuta el scrip de carga
                        cwd='./load') #que lo ejecute en la carpeta './load'
        subprocess.run(['rm', clean_data_filename], #una vez cargado en sqlite, borramos el archivo
                        cwd='./load') #que lo ejecute en la carpeta './load'

if __name__ == '__main__':
    main()
