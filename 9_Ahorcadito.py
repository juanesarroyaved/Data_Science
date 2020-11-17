# -*- coding: utf-8 -*-

import random

IMAGES = ['''

    +---+
    |   |
        |
        |
        |
        |
        ======''','''

    +---+
    |   |
    0   |
        |
        |
        |
        ======''','''	

    +---+
    |   |
    0   |
    |   |
        |
        |
        ======''','''

    +---+
    |   |
    0   |
   /|   |
        |
        |
        ======''','''

    +---+
    |   |
    0   |
   /|\  |
        |
        |
        ======''','''

    +---+
    |   |
    0   |
   /|\  |
    |   |
        |
        ======''','''

    +---+
    |   |
    0   |
   /|\  |
    |   |
   /    |
        ======''','''

    +---+
    |   |
    0   |
   /|\  |
    |   |
   / \  |
        ======''','''

''']

WORDS = [
	'lavadora',
	'secadora',
	'sofa',
	'putito',
	'cabron',
	'porky',
	'gorra',
]

def display_board(hidden_word, tries):
	print(IMAGES[tries])
	print('')
	print(hidden_word)
	print('---*---*---*---*---*---')

def random_word():
	idx = random.randint(0, len(WORDS) - 1) #debemos importal em módulo random
	return WORDS[idx]

def run():
	word = random_word()
	hidden_word = ['-'] * len(word)
	tries = 0

	while True:
		display_board(hidden_word,tries)
		current_letter = str(input('Escoge una letra: '))

		letter_indexes = []
		for idx in range(len(word)):
			if word[idx] == current_letter:
				letter_indexes.append(idx)

		if len(letter_indexes) == 0:
			tries += 1

			if tries == 7:
				display_board(hidden_word, tries)
				print('')
				print('PERDISTE PUTOOOOOO!!! La palabra era {}'.format(word))
				break

		else:
			for idx in letter_indexes:
				hidden_word[idx] = current_letter

		try:
			hidden_word.index('-')
		except ValueError:
			print('')
			print('AY CABRÓN, PERO SI GANASTE WEY 8===============D. Era {}'.format(word))

if __name__ == '__main__':

	print('B I E N V E N I D O S   P U T I T O S')
	run()