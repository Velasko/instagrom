from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

from .. import dynamo

from . import like

class DynamoTable():

	def __init__(self, table_name, **where):
		self.struct = like.Like
		self.where = where
		self.table = dynamo.tables[table_name]

	def append(self, **kwargs):
		obj = self.struct(**kwargs)
		
		if obj in self:
			raise KeyError('Object already in table')

		self.table.put_item(Item=kwargs)

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

		if len(where) == 0:
			table = self.table.scan()['Items']

		elif len(where) == 1:

			key, value = list(where.items())[0]

			table = self.table.scan(
				FilterExpression=Attr(key).eq(value)
				)['Items']


		elif len(where) == 2:
			try:
				item = self.table.get_item(Key=where)['Item']
				return [self.struct(**item)]

			except KeyError:
				return []
			except ClientError:
				raise KeyError("Unexpected error! Maybe you used a wrong database key.")


		return [self.struct(**item) for item in table]

	def delete(self, item):
		self.table.delete_item(Key=item.serialize())

	def __str__(self):
		return self.get().__str__()

	def __iter__(self):
		return self.get().__iter__()

	def __len__(self):
		return self.get().__len__()

	def __getitem__(self, index):
		return self.get()[index]