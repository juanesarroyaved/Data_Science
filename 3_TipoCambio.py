# -*- coding: utf-8 -*-

def run():
	print('C A L C U L A D O R A  D E  D I V I S A S')
	print('')

	ammount = float(input('Ingrese la cant. de pesos mexicanos a convertir: '))

	result = foreign_exchange_calculator(ammount)

	print('${} pesos mexicanos son ${} pesos colombianos'.format(ammount, result))

def foreign_exchange_calculator(ammount):
	mex_to_col_rate = 145.97

	return mex_to_col_rate * ammount


if __name__ == '__main__':
	run()