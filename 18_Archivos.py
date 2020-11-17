# -*- coding: utf-8 -*-

def run():
	with open('numeros.txt','a') as f:
		for i in range(10):
			f.write(str(i))
	f.close()

	counter = 0
	palabra = str(input('Escriba una palabra que quiera encontrar: '))
	with open('aleph.txt', encoding="utf-8") as aleph:
		for i in aleph:
			counter += i.count(palabra)
		print('La palabra {} se encuentra {} veces en el texto.'.format(palabra, counter))

if __name__ == '__main__':
	run()