import dataclasses
from .basicitem import BasicItem

@dataclasses.dataclass
class User(BasicItem):
	nick : str
	name : str
	password : str
	email : str
	profile_picture : str

	def get_keys(self):
		return 'nick'

	def get_posts(self):
		from . import database
		return database.get_posts(user=self.nick)

	def get_likes(self):
		from . import database
		return database.get_likes(user=self.nick)