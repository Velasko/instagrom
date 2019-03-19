from flask import session, redirect, url_for

from .login import Login

def main(request):
	login = Login()

	if login.check(request.form):
		session['username'] = request.form['username']
		return redirect(url_for('user_feed'))
	else:
		login.fail()
		return redirect(url_for('login'))