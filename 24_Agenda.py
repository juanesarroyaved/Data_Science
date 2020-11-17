# -*- coding: utf-8 -*-

import csv

class Contact:

	def __init__(self, name, phone, email): #Método constructor. Los métodos de las clases empiezan con "self"
		self.name = name
		self.phone = phone
		self.email = email

class ContactBook:

	def __init__(self):
		self._contacts = []

	def add(self, name, phone, email):
		contact = Contact(name, phone, email)
		self._contacts.append(contact)
		self._save()

	def show_all(self):
		for contact in self._contacts:
			self._print_contact(contact)

	def _print_contact(self, contact):
		print('----------------------------------------------------------')
		print('Name: {}'.format(contact.name))
		print('Phone: {}'.format(contact.phone))
		print('Email: {}'.format(contact.email))
		print('----------------------------------------------------------')

	def _delete(self, name):
		for idx, contact in enumerate(self._contacts):
			if name.lower() == contact.name.lower():
				del self._contacts[idx]
				self._save()
				break

	def search(self, name):
		for contact in self._contacts:
			if contact.name.lower() == name.lower():
				self._print_contact(contact)
				break
		else: #Es un else que pertenece al For y es para indicar que no lo encontramos
			self._not_found()

	def _not_found(self):
		print('-----------------------')
		print('Contacto no encontrado.')
		print('-----------------------')

	def _save(self):
		with open('contacts.csv', 'w') as f:
			writer = csv.writer(f)
			writer.writerow(('name','phone','email'))
			for contact in self._contacts:
				writer.writerow((contact.name,contact.phone,contact.email))

def run():

	contact_book = ContactBook()

	with open('contacts.csv', 'r') as f:
		reader = csv.reader(f)
		for idx, row in enumerate(reader):
			if idx == 0 or row == []:
				continue
			
			contact_book.add(row[0], row[1], row[2])

	while True:
		command = str(input('''
			¿Qué deseas hacer?

			[a]ñadir contacto
			[ac]ctualizar contacto
			[b]uscar contacto
			[e]liminar contacto
			[l]istar contactos
			[s]alir
		'''))

		if command == 'a':
			name = str(input('Nombre del contacto: '))
			phone = str(input('Teléfono del contacto:'))
			email = str(input('Email del contacto: '))

			contact_book.add(name, phone, email)


		elif command == 'ac':
			print('actualizar contacto')

		elif command == 'b':
			name = str(input('Contacto a buscar: '))
			contact_book.search(name)

		elif command == 'e':
			name = str(input('Contacto a eliminar: '))

			contact_book._delete(name)
			contact_book.show_all()

		elif command == 'l':
			contact_book.show_all()

		elif command == 's':
			break

		else:
			print('Comando no encontrado')


if __name__ == '__main__':
	print('BIENVENIDO A LA AGENDA')
	run()