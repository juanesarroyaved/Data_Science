if __name__ == '__main__':


	calificaciones = {}
	calificaciones['algoritmos'] = 9
	calificaciones['algebra'] = 10
	calificaciones['web'] = 8
	calificaciones['BDs'] = 10

	suma_calificaciones = 0

	for key in calificaciones:
		print(key)
	for values in calificaciones.values():
		print(values)
	for key, values in calificaciones.items(): #en python 2 es .iteritems()
		print('llave: {}, valor: {}'.format(key, values))

	for calificacion in calificaciones.values():
		suma_calificaciones += calificacion

	promedio = suma_calificaciones / len(calificaciones.values())

	print(promedio)
