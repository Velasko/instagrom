import datetime
import dataclasses
from .basicitem import BasicItem

@dataclasses.dataclass
class Post(BasicItem):
	user : str
	text : str
	image : str
	datetime : str = None
	id : int = 0

	def auto_key(self):
		if self.datetime == None:
			self.datetime = datetime.datetime.now()

	def get_keys(self):
		return 'id'

	def get_user(self):
		from . import database
		return database.get_users(nick=self.user)

	def get_likes(self):
		from . import database
		return database.get_likes(post=self.id)