from flask import session

from .. import app

@app.route("/feed")
def user_feed():
	return f"aqui está seu feed, {session['username']}"