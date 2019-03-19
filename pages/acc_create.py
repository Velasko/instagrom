from flask import request, session, redirect, url_for


from .. import app
from ..auth import new

@app.route("/new_account", methods=['GET', 'POST'])
def new_account():
	if request.method == 'POST':
		return new.create_account(request.form)

	return 	"""<form method="post">
		Nick:
			<p><input type=text name=username><p>
		Full Name:
			<p><input type=text name=name><p>
		E-Mail:
			<p><input type=text name=email><p>
		Password:
			<p><input type=password name=password><p>
		Password check
			<p><input type=password name=pass_check><p>
			<p><input type=submit value=create account>
		</form>"""
