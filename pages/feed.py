from flask import session
from flask import render_template
from ..database import database as db
from .. import app


@app.route("/feed")
def user_feed():
	table = db.get_posts()
	return render_template('feed.html', username=session['username'], posts=table)

