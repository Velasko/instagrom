from dataclasses import dataclass
from .. import database

class BasicTable():
	db = database.database

	def __init__(self, table_name, object_class, **where):
		"""Table_name : str = table name in the database
		object_class : object = an instanciated class which represents a row in the table
		where : **dict = containing the restrictions of the table when using the getter method
		"""

		self.table = table_name
		self.struct = object_class
		self.where = where

	def append(self, *args, **kwargs):
		"""Instanciates and adds to the database 
		the object of the current table.

		Look for the object's instanciation to know the parameters
		which should be passed.

		In case the object is already in the table (a row already have the
		same key attributes), then an error is raised (KeyError).
		Unless "update=True" is passed as a parameter aswell.
		This would, instead, update the row in the database.
		"""

		#Checking if, in case of existance, if must update the
		#database instead of rasing an error
		if 'update' in kwargs:
			update = kwargs['update']
			del kwargs['update']
		else:
			update = False

		obj = self.struct(*args, **kwargs)

		try:
			BasicTable.db.add(self.table, obj)
			return self[-1]
		except KeyError as e:
			if update:
				return BasicTable.db.update(self.table, obj)
			else:
				raise KeyError(e)

	def __iter__(self):
		return self.get().__iter__()

	def __getitem__(self, index):
		return BasicTable.db.get_table(self.table, self.struct, **self.where).__getitem__(index)

	def get(self, **kwargs):
		"""kwargs is the sql 'where' parameter
		The parameters are passed on the form id=1.

		If the table has been instanciated with a where, then it
		must not have an attribute conflict, as in table ask for
		id=3 and this get searches for an id=4.

		IF there is such conflict, an AttributeError shall be rased.
		""" 

		#cheking if there is a key error in current get and the table
		for key in self.where.keys():
			try:
				kwargs[key]
			except KeyError:
				#No conflict so far
				pass
			else:
				#Ambiguous where.
				#Say if this table has where user = potato
				#Then this get mustn't have a user != potato
				if kwargs[key] != self.where[key]: 
					raise AttributeError(f"Ambiguous where. Can't decide if '{key}' should be '{self.where[key]}' or '{kwargs[key]}'")

		#Concatenating both wheres
		where = {**self.where, **kwargs}

		return BasicTable.db.get_table(self.table, self.struct, **where)

	def __str__(self):
		return self.get().__str__()

	def __len__(self):
		return self.get().__len__()