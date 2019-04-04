from flask import render_template, session, request, redirect, url_for


from .. import app
from ..database import database as db
from ..resources import get_bucket
from ..models.forms import SigninForm

@app.route('/profile/<username>')
def profile(username):
    users = db.get_users()
    user = users.get(nick=username)[0]
    if (username == session['username']):
        return render_template('private_profile.html', user=user)
    else:
        posts = db.get_posts(user=username)
        return render_template('public_profile.html', user=user, posts=posts)

@app.route('/update_profile_pic', methods=['POST'])
def update_profile_pic():
    username = session['username']

    users = db.get_users()
    user = users.get(nick=username)[0]
    password = request.form['password']

    if user.password == password:
        file = request.files['file']
        file_extension = file.filename.split('.')[1]
        file.filename = f'instagrom/{user.nick}/profile_picture.{file_extension}'
        print(file.filename)

        my_bucket = get_bucket()
        my_bucket.Object(file.filename).put(Body=file)

        user.profile_picture = file.filename

        users.append(**user.serialize(), update=True)

    else:
        print('Operação não autorizada')

    return redirect(url_for('profile', username=username))