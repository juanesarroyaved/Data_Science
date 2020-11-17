import turtle #en sublime text ejecutar Ctrl + Shft + B

def main():
	window = turtle.Screen()
	dave = turtle.Turtle()

	make_square(dave)

	turtle.mainloop() #que no cierre la pantalla cuando termine

def make_square(dave):
	lenght = int(input('Tamaño cuadrado: '))

	for i in range(4):
		make_line_and_turn(dave,lenght)

def make_line_and_turn(dave, lenght):
	dave.forward(lenght)
	dave.left(90)

if __name__ == '__main__': #pyhton siempre llama main a los archivos que abre. Le estamos diciendo donde debe empezar
	main()