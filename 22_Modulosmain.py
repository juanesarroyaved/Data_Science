# -*- coding: utf-8 -*-

#Dos formas de correrlo:
#1. import lamp
#	lamp = lamp.Lamp(is_turned_on = True)
#
#2. from lamp import Lamp

#utilizaremos la segunda opción:

from Moduloslamp import Lamp

def run():
	lamp = Lamp(is_turned_on = True)

	while True:
		command = str(input('''
			¿Qué desea hacer?

			[p]render
			[a]pagar
			[s]alir
		'''))

		if command == 'p':
			lamp.turn_on()
		elif command == 'a':
			lamp.turn_of()
		else:
			break

if __name__ == '__main__':
	run()