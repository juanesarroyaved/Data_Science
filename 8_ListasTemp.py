# -*- coding: utf-8 -*-

def average_temps(temps):
	sum_of_temps=0

	for temp in temps:
		sum_of_temps += temp #OJO: le sumo temp y NO temps porque sumo un valor y no la lista.

	return sum_of_temps / len(temps)

if __name__ == '__main__': 
	temps = [21, 24, 24, 22, 20, 23, 24]

	temps.append(int(input('Ingresa la temperatura de hoy: ')))

	average = average_temps(temps)

	print('La temperatura promedio es {}'.format(average))