from flask import render_template, session, request, redirect, url_for


from .. import app
from ..database import database as db

@app.route('/search', methods=['GET', 'POST'])
def search():
    found_users=None
    if request.method=='POST':
        username = request.form['username']
        users = db.get_users()
        found_users = users.like(username)

    return render_template('search.html', users=found_users)
