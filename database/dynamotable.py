from .. import database
from .. import dynamo

from . import like

class DynamoTable():

	def __init__(self, **where):
		self.struct = like.Like
		self.where = where
		self.table = dynamo.tables['Likes']

	def append(self, **kwargs):
		obj = self.struct(**kwargs)
		
		if obj in self:
			raise KeyError('Object already in table')

		self.table.put_item(item=kwargs)

	def get(self, **kwargs):
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

		if len(where) <= 1:
			table = self.table.scan(*where.values())['Items']
		else:
			table = self.table.get_item(Key=where.values())['Items']

		return [self.struct(**item) for item in table]

	def delete(self, item):
		self.table.delete_item(Key=item.serialize())

	def __str__(self):
		return self.get().__str__()

	def __iter__(self):
		return self.get().__iter__()