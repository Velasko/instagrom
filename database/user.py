import dataclasses

from .basicitem import BasicItem
from .basictable import BasicTable
from . import levenshtein

@dataclasses.dataclass
class User(BasicItem):
	nick : str
	name : str
	password : str
	email : str
	profile_picture : str = 'instagrom/placeholder.png'

	def get_keys(self):
		return 'nick'

	def get_posts(self):
		from . import database
		return database.get_posts(user=self.nick)

	def get_likes(self):
		from . import database
		return database.get_likes(user=self.nick)

	def __lt__(self, other):
		if not isinstance(other, type(self)): return False

		return self.nick.__lt__(other.nick)


class UserTable(BasicTable):
	def like(self, query_name : str, distance=3, case_sensitive=False):
		"""Returns a list of Users in which needs less or equal {distance}
		changes to be equal to the query_name.

		query_name : str
		distance : int = 3
		case_sensitive : boolean = False"""
		users = BasicTable.db.get_table(self.table, self.struct)

		if not case_sensitive:
			query_name = query_name.lower()

		users_like = { i : [] for i in range(distance)}
		for user in users:


			dist = levenshtein.distance(
				query_name,
				user.nick,
				case_sensitive=case_sensitive,
				)

			if dist <= distance:
				users_like[dist].append(user)

		for values in users_like.values():
			values.sort()

		return [ item for key, value in users_like.items() for item in value]