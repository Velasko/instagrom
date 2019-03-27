from flask import redirect, url_for, session

from .. import app

@app.route("/index.html")
@app.route("/")
def index():
	if 'username' in session:
		return redirect(url_for('user_feed'))

	return redirect(url_for('login'))