from flask import render_template, session, request, redirect, url_for


from .. import app
from ..database import database as db
from ..resources import get_bucket
from ..models.forms import UpdateForm

@app.route('/profile/<username>')
def profile(username):
    users = db.get_users()
    user = users.get(nick=username)[0]
    posts = db.get_posts(user=username)
    return render_template('public_profile.html', user=user, posts=posts)

@app.route('/update_profile/<username>', methods=['GET', 'POST'])
def update_profile(username):
    users = db.get_users()
    user = users.get(nick=username)[0]

    form = UpdateForm()

    return render_template('private_profile.html', user=user, form=form)

@app.route('/update_profile_info/<username>', methods=['POST'])
def update_profile_info(username):
    if request.method == 'POST':
        if request.form['password'] == request.form['pass_check']:
            file = request.files['file']
            file_extension = file.filename.split('.')[1]
            file.filename = f'instagrom/{username}/profile_picture.{file_extension}'


            my_bucket = get_bucket()
            my_bucket.Object(file.filename).put(Body=file)

            name = request.form['name']
            email = request.form['email']
            password = request.form['password']

            updated_user = {
                'nick': username,
                'name': name,
                'email': email,
                'password': password,
                'profile_picture': file.filename
            }

            users = db.get_users()
            users.append(**updated_user, update=True)

    return redirect(url_for('profile',username=username))

