from flask import request, session, redirect, url_for, render_template

from ..models.forms import SigninForm
from .. import app
from ..auth import new

@app.route("/new_account", methods=['GET', 'POST'])
def new_account():

	if request.method == 'POST':
		return new.create_account(request.form)

	form = SigninForm()

	return render_template('signin.html', form=form)
