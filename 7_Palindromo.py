# -*- coding: utf-8 -*-

def palindromo(palabra):

	reversed_letters = []

	for letter in palabra:
		reversed_letters.insert(0, letter)
	reversed_word = ''.join(reversed_letters)

	if reversed_word == palabra:
		return True

	return	False

if __name__ == '__main__':
	
	palabra = str(input('Escribe la palabra que quieras comprobar: '))

	result = palindromo(palabra)

	if result == True:
		print('{} si es un palindromo'.format(palabra))
	else:
		print('{} NO es un palindromo'.format(palabra))

# FORMA MÁS FÁCIL:
#if __name__ == '__main__':
#	p = 'ojazo'

#	if p[::-1] == p:
#		print('SI lo es')
#	else:
#		print('NO lo es')
