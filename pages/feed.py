from .. import app

@app.route("/feed")
def user_feed():
	return "aqui está seu feed"