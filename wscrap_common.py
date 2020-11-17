import yaml #yaml es una especie de archivo JSON pero sin tanto ruido visual


__config = None

def config():
	global __config #la defino como global para poder usarla en otros módulos
	if not __config:
		with open('config.yaml', mode='r') as f: #abro el archivo yaml en modo lectura y lo denomino f
			__config = yaml.safe_load(f) #cargo el contenido del archivo yaml

	return __config
