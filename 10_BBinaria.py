# -*- coding: utf-8 -*-

def binary_search(numbers, number_to_find, low, high):
	
	if low > high:
		return False

	mid = int((low + high) / 2)

	if numbers[mid] == number_to_find:
		return True
	elif numbers[mid] > number_to_find:
		return binary_search(numbers, number_to_find, low, mid - 1)
	else:
		return binary_search(numbers, number_to_find, mid + 1, high)

if __name__ == '__main__':
	
	numbers = [2,3,4,6,7,9,12,14,17,18,19]

	number_to_find = int(input('Seleccione un número a encontrar de acá {}:'.format(numbers)))

	result = binary_search(numbers, number_to_find, 0, len(numbers)-1)

	if result is True:
		print('El número {} si está en la lista'.format(number_to_find))
	else:
		print('El número {} NO está en la lista'.format(number_to_find))
