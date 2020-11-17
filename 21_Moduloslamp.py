# -*- coding: utf-8 -*-

class Lamp:

	_LAMPS = ['''
          .
     .    |    ,
      \   '   /
       ` ,-. '
    --- (   ) ---
         \ /
        _|=|_
       |_____|
    ''',
    '''
         ,-.
        (   )
         \ /
        _|=|_
       |_____|
    ''']

	 #__init__ Constructor de la clase: primer método que se ejecuta cuando generamos una nueva instancia.
	def __init__(self, is_turned_on): #Método de instancia: self (propia instancia).
		self._is_turned_on = is_turned_on

	def turn_on(self):
		self._is_turned_on = True
		self._display_image()

	def turn_of(self):
		self._is_turned_on = False
		self._display_image()

	def _display_image(self): #Método privado porque queremos esconder la complejidad
		if self._is_turned_on:
			print(self._LAMPS[0])
		else:
			print(self._LAMPS[1])