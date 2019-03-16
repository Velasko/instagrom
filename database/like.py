import dataclasses
from .basicitem import BasicItem

@dataclasses.dataclass
class Like(BasicItem):
	user : str
	post : int

	def get_keys(self):
		return 'user', 'post'

	def get_user(self):
		from . import database
		return database.get_users(nick=self.user)

	def get_post(self):
		from . import database
		return database.get_posts(id=self.post)