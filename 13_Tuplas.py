if __name__ == '__main__':
	mi_tupla = (1,2,3,4) #con () se hacen tuplas
	tipotupla = type(mi_tupla)
	print(tipotupla)

	mi_lista = [1,2,3,4] # con [] se hacen listas
	tipolista = type(mi_lista)
	print(tipolista)
	
	mi_lista[0]=999 #las listas si se pueden modificar
	print(mi_lista)

	nueva_tupla = (1,) #para crear una tupla con un solo valor se debe añadir coma al final, si no lo toma como un entero (int)

	tiponuevatupla = type(nueva_tupla)
	print(tiponuevatupla)

	nueva_tupla2 = nueva_tupla + (2,3,4)

	print(nueva_tupla2)
