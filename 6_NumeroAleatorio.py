# -*- coding: utf-8 -*-

import random

def aleatorio():
	number_found = False

	while not number_found:
		
		number_random = random.randint(0,5)

		number = int(input('Intenta adivinar el número: '))

		if number == number_random:
			print('FELICIDADES!!! Acertaste el número cabrón')

			number_found = True

if __name__ == '__main__':
	aleatorio()
