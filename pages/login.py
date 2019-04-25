from flask import request, session, redirect, url_for, render_template
from ..models.forms import LoginForm

from .. import app
from .. import auth

@app.route("/login", methods=['GET', 'POST'])
def login():
#	print(help(url_for))
	form = LoginForm()
	if request.method == 'POST':
		return auth.check(request)


	page_base = '''<form method="post">
		Nick:
			<p><input type=text name=username><p>
		Password:
			<p><input type=password name=password><p>
			<p><input type=submit value=Login>
		</form>
		<form action="/new_account" method="get">
			<input type="submit" value="Don't have an account?"/>
		</form>
	'''

	if auth.status.attempts > 0:
		page_base = "login failed" + page_base

	return render_template('login.html', form=form)


@app.route('/logout')
def logout():
	if 'username' not in session:
		return redirect(url_for('login'))
	# remove the username from the session if it's there
	session.pop('username', None)
	session.pop('attempt', None)
	return redirect(url_for('index'))