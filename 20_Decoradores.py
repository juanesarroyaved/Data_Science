# -*- coding:utf-8 -*-

def protected(func): #Paso 4

	def wrapper(password): #Paso 5
		if password == 'platzi': #Paso 6
			return func() #Paso 6.1
		else:
			print('La contraseña es incorrecta.') #Paso 6.2

	return wrapper #Paso 7

@protected #Paso 3: estamos protegiendo una función (protected_fun) para que se ejecute solo ante una condición.
def protected_fun(): #Paso 6.1.1
	print('Tu contraseña es correcta.') #Paso 6.1.1.1

if __name__ == '__main__':
	password = str(input('Ingresa tu contraseña: ')) #Paso 1: se ingresa contraseña

	protected_fun(password) #Paso 2: va a ejecutar la función protected_fun() pero su ejecución está atada al decorador @protected 
