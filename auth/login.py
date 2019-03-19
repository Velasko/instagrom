import datetime
from flask import session, redirect, url_for

from .hash import passwd_hash
from ..database import database as db

class Login():
	attempts = 0
	last_try = None

	def check(self, form):
		"""Recieves a dict with 'username' and 'password' keys
		and verifies the authentication."""

		#get user
		users = db.get_users(nick=form['username'])

		#len(users) == 1 -> There is such user, and there is no ambiguity
		if len(users) == 1 and self.password_check(users[0], form['password']):
			self.success()
			return True
		else:
			self.fail()
			return False

	def password_check(self, user, passwd):
		"""Checks if this is the user's password"""
		return user.password == passwd_hash(passwd)

	def success(self):
		Login.attempts = 0
		Login.last_try = None

	def fail(self):
		Login.attempts += 1
		Login.last_try = datetime.datetime.now()
