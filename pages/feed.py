from flask import session, render_template, redirect, url_for, request

from ..resources import get_bucket, generate_key_string

from .. import app
from ..database import database as db
from ..models.forms import PostForm


@app.route("/feed", methods=['GET', 'POST'])
def user_feed():
	form = PostForm()

	posts = db.get_posts()
	likes = db.get_likes()

	my_bucket = get_bucket()
	summaries = my_bucket.objects.all()

	if form.validate_on_submit():
		post = {'user': session['username'], 'image': form.content.data}
		posts.append(**post)
		return redirect(url_for('user_feed'))


	return render_template('feed.html', form=form, posts=posts, likes=likes, summaries=summaries)

@app.route('/like/<user>/<int:post_id>', methods=['GET', 'POST'])
def like(user, post_id):

	likes = db.get_likes(post=post_id)

	exists = False

	for like in likes:
		if like.user==user:
			exists = True

	if not exists:
		new_like = {
			'user': user,
			'post': post_id
		}

		likes.append(**new_like)
	else:
		print("Like já existente!")

	return redirect(url_for('user_feed'))

@app.route('/upload', methods=['POST'])
def upload():
	user = session['username']

	file = request.files['file']
	file_extension = file.filename.split('.')[1]
	print(file.filename)
	key_string = generate_key_string()
	file.filename = f'instagrom/{user}/{key_string}.{file_extension}'
	my_bucket = get_bucket()
	my_bucket.Object(file.filename).put(Body=file)

	posts = db.get_posts()
	post = {
		'user': user,
		'image': file.filename
	}
	posts.append(**post)

	return redirect(url_for('user_feed'))