from flask import request, session, redirect, url_for

from . import hash
from ..database import database as db

def create_account(form):
	if form['password'] != form['pass_check']:
		return 'diff password'

	new_user = {
	'nick' : form['username'],
	'name' : form['name'],
	'password' : hash.passwd_hash(form['password']),
	'email' : form['email'],
	'profile_picture' : None
	}

	users = db.get_users()
	try:
		users.append(**new_user)
	except KeyError:
		return "Username in use"
	else:
		session['username'] = request.form['username']
		return redirect(url_for('user_feed'))
		return "successful"