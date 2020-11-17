# -*- coding: utf-8 -*-

KEYS = {
	'a' : '1',
	'b' : '2',
	'c' : '3',
	'd' : '4',
	'e' : '5',
	'f' : '6',
	'g' : '7',
	'h' : '8',
	'i' : '9',
	'j' : '0',
	'k' : 'z',
	'l' : 'x',
	'm' : 'y',
	'n' : 'w',
	'o' : 't',
	'p' : 'u',
	'q' : 'r',
	'r' : 'a',
	's' : 'b',
	't' : 'c',
	'u' : 'e',
	'v' : 'h',
	'w' : '.',
	'x' : 'r',
	'y' : '#',
	'z' : 'q',
}

def cypher(message):
	words = message.split(' ')
	cypher_message = []

	for word in words:
		cypher_word = ''

		for letter in word:
			cypher_word += KEYS[letter]

		cypher_message.append(cypher_word)

	return ''.join(cypher_message)

def decypher(message):
	words = message.split(' ')
	decypher_message = []

	for word in words:
		decypher_word = ''

		for letter in word:
			
			for key, value in KEYS.items():
				if value == letter:
					decypher_word += key

		decypher_message.append(decypher_word)

	return ''.join(decypher_message)

def run():

	while True:

		command = str(input(''' --- * --- *--- *--- *

			Bienvenido a criptografía, ¿qué deseas hacer?

			[c]ifrar mensaje
			[d]escifrar mensaje
			[s]alir
		'''))

		if command == 'c':
			message = str(input('escriba su mensaje cabrón: '))
			cypher_message = cypher(message)
			print(cypher_message)
		elif command == 'd':
			message = str(input('Escribe tu mensaje cifrado: '))
			decypher_message = decypher(message)
			print(decypher_message)
		elif command == 's':
			break
		else:
			print('¡Comando no encontrado puto!')
			break

if __name__ == '__main__':
	print('MENSAJES CIFRADOS')
	run()
