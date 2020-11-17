import yaml #cargamos el modulo de yaml instalado como conda install pyyaml

__config = None #variable global (se inicializa con __vble) porque estamos leyendo a disco


def config():
    global __config #La definimos como vble para usar la vble en otros módulos o funciones
    if not __config: #si no tenemos la configuración hacemos lo siguiente
        with open('config.yaml', mode='r') as f: #abrimos .yaml en modo lectura y lo nombramos f
            __config = yaml.load(f) #cargamos el archivo .yaml con el módulo yaml importado

    return __config #devuelve la configuración
