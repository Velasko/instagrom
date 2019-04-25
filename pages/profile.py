from flask import render_template, session, request, redirect, url_for
from google.cloud import storage

from .. import app
from ..database import database as db
from ..models.forms import UpdateForm
from ..filters import file_type


@app.route('/profile/<username>')
def profile(username):

    users = db.get_users()
    user = users.get(nick=username)[0]
    posts = db.get_posts(user=username)

    file_types = []
    for post in posts:
        file_types.append(file_type(post.image))

    return render_template('public_profile.html', user=user, posts=posts, file_types=file_types)


@app.route('/update_profile/<username>', methods=['GET', 'POST'])
def update_profile(username):
    if 'username' not in session:
        return redirect(url_for('login'))
    users = db.get_users()
    user = users.get(nick=username)[0]

    form = UpdateForm()

    return render_template('private_profile.html', user=user, form=form)


@app.route('/update_profile_info/<username>', methods=['POST'])
def update_profile_info(username):
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        if request.form['password'] == request.form['pass_check']:
            file = request.files['file']
            file_extension = file.filename.split('.')[1]
            file.filename = f'profile_pictures/{username}-profile_picture.{file_extension}'

            gcs = storage.Client()
            bucket = gcs.get_bucket('instagrom')
            blob = bucket.blob(file.filename)
            blob.upload_from_string(
                file.read(),
                content_type=file.content_type
            )

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

    return redirect(url_for('profile', username=username))


