from flask import render_template

from .. import app

@app.route("/index.html")
@app.route("/")
def index():
	return render_template('index.html')