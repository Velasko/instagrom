import logging
import datetime
import pymysql as sql

from ..settings import database_auth as auth
from ..system import slash

class Database():
	def __init__(self):
		logging.info('Starting database at {}'.format(datetime.datetime.now()))
		self.conn = None

#---START OF DATABASE CONNECTION METHODS BLOCK---------------------------------------
	def start(self):
		# starting db connection
		self.conn = sql.connect(
			*auth,
			connect_timeout=5
			)
#		 logging.info('Aplication database has connected')

	def close(self):
		#closing db connection
		if self.conn is not None:
			self.conn.close()
#			logging.info('Aplication database has disconnected')

			self.conn = None
		else:
#			logging.warning('Requested to close a database connection while not connected')
			pass
#---END OF DATABASE CONNECTION METHODS BLOCK---------------------------------------


#---START OF SQL QUERY METHODS BLOCK---------------------------------------
	def get_table(self, table, obj_struct, **where):

		where = self.get_where(where)

		try:
			self.start()

			with self.conn.cursor() as cursor:
				cursor.execute(f'SELECT * FROM {table} {where}')
				dbobject = cursor.fetchall()

			data = [obj_struct(*row) for row in dbobject]
			return data

		finally:
			self.close()

	def add(self, table, data):

		data = data.serialize()

		#In case it's a autoincrement id:
		try:
			if data['id'] == 0:
				del data['id']
		except KeyError:
			pass

		columns, attributes = list(data.keys()), list(data.values())
		question_marks = ', '.join(['%s' for _ in columns])
		columns = ", ".join(columns)

		try:
			self.start()
			with self.conn.cursor() as cursor:
				cursor.execute(f'INSERT INTO {table}({columns}) VALUES ({question_marks})', attributes)
			self.conn.commit()
		except sql.err.IntegrityError as e:
			raise KeyError(e)
		finally:
			self.close()

	def update(self, table, data):

		keys = data.get_keys()
		print(f"p-keys: {keys}")
		data = data.serialize()

		set = []
		attributes = []
		where = {}
		for key, value in data.items():
			if key in keys:
				where[key] = value
			else:
				set.append(f"{key} = %s")
				attributes.append(value)

		#Where has be the table keys
		where = self.get_where(where)
		set = ', '.join(set)

		try:
			self.start()
			with self.conn.cursor() as cursor:
				cursor.execute(f"UPDATE {table} SET {set} {where}", attributes)
			self.conn.commit()
		finally:
			self.close()
#---END OF SQL QUERY METHODS BLOCK---------------------------------------


#---START USEFUL METHODS BLOCK---------------------------------------
	def isotime_to_datetime(self, data):
		return datetime.datetime.fromisoformat(data)

	def get_where(self, where):
		""""Given a dict (where), returns the 'where' parameter of a SQL query"""
		if where == {}: return ''

		for key, value in where.items():
			if isinstance(value, str):
				where[key] = f"'{value}'"
		return f"WHERE {'AND '.join([f'{key}={value}' for key, value in where.items()])}"
#---END USEFUL METHODS BLOCK---------------------------------------


#---START OF GET TABLE METHODS BLOCK---------------------------------------
	def get_users(self, **where):
		from . import basictable, user
		table = basictable.BasicTable('users', user.User, **where)
		del basictable, user
		return table

	def get_posts(self, **where):
		from . import basictable, post
		table = basictable.BasicTable('posts', post.Post, **where)
		del basictable, post
		return table

	def get_likes(self, **where):
		from . import basictable, like
		table = basictable.BasicTable('likes', like.Like, **where)
		del basictable, like
		return table


#---END OF GET TABLE METHODS BLOCK---------------------------------------

if __name__ == '__main__':
	print('START OF MAIN DB\n')
	db = Database()
	table = db.get_users()

#	table.append('Velasco', 'luis', '1235', 'f@gmail', 'pfp', update=True)
	for item in table:
		print(item)


	'''
	tablel = db.get_likes()
	print(tablel)
#	items = table.get()
	user = table.get(nick='rhan')
	print(user)
	posts = user[0].get_posts()
	print(posts)
	like = posts[0].get_likes()
	print(like)
	# for item in table:
	# 	print(item, 'in main')
	# 	print()
	# 	for post in item.get_posts():
	# 		print(post, 'in main')
	# 	print()
	'''
	print('\nEND OF MAIN DB')