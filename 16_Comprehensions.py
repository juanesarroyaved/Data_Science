# -*- coding: utf-8 -*-

if __name__ == '__main__':

	#Creando una lista de pares con el método TRADICIONAL

	pares = []
	for num in range(100):
		if num % 2 == 0:
			pares.append(num)

	print(pares)

	#Creando un Diccionario con el método TRADICIONAL

	squares = {}

	for x in range(100):
		squares[x] = x**2

	print(squares)

	#Creando una lista con List Comprehension (también llamados Sintactic Sugars)

	impares = [x for x in range(100) if x % 2 != 0]

	print(impares)

	#Creando un Diccionario con Dictionary Comprehension

	cuadrados = {x: x**2 for x in range(100)}

	print(cuadrados)