from flask import session, render_template, redirect, url_for, request

from ..resources import get_bucket
from ..filters import file_type

from .. import app
from ..database import database as db
from ..models.forms import PostForm

import datetime

def filter_posts(posts, startdate, finaldate):

	filtered_posts = []
	startdate = datetime.datetime.strptime(startdate, '%Y-%m-%dT%H:%M').strftime('%Y-%m-%dT%H:%M')
	finaldate = datetime.datetime.strptime(finaldate, '%Y-%m-%dT%H:%M').strftime('%Y-%m-%dT%H:%M')
	for post in posts:
		date = datetime.datetime.strptime(post.datetime, '%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m-%dT%H:%M')

		if (date >= startdate) & (date <= finaldate):
			filtered_posts.append(post)


	return filtered_posts

@app.route("/feed", methods=['GET', 'POST'])
def user_feed():
	form = PostForm()

	posts = db.get_posts()
	likes = db.get_likes()

	my_bucket = get_bucket()
	summaries = my_bucket.objects.all()
	post_title = 'Posts Recentes'
	if request.form:
		startdate = request.form['startdate']
		finaldate = request.form['finaldate']
		posts = filter_posts(posts, startdate, finaldate)
		post_title = f'Posts Filtrados'

	if form.validate_on_submit():
		post = {'user': session['username'], 'image': form.content.data}
		posts.append(**post)
		return redirect(url_for('user_feed'))

	file_types = []
	for post in posts:
		file_types.append(file_type(post.image))

	return render_template('feed.html', form=form, posts=posts, likes=likes, summaries=summaries, post_title=post_title, file_types=file_types)

@app.route('/like/<user>/<int:post_id>/<redirect_to>', methods=['GET', 'POST'])
def like(user, post_id, redirect_to):

	likes = db.get_likes(post=post_id)
	try:
		like = likes.get(user=user)[0]
	except IndexError:
		likes.append(user=user, post=post_id)
	else:
		likes.delete(like)

	redirect_user = db.get_posts(id=post_id)[0].user

	if redirect_to == 'profile':
		return redirect(url_for('profile', username=redirect_user))
	else:
		return redirect(url_for('user_feed'))

@app.route('/post')
def post():
	if 'username' in session:
		return render_template('post.html')
	else:
		return render_template('login.html')


@app.route('/upload', methods=['POST'])
def upload():
	user = session['username']

	user_posts_count = db.get_posts(user=user).__len__() + 1

	if request.files['file']:
		file = request.files['file']
		file_extension = file.filename.split('.')[1]
		file.filename = f'instagrom/{user}/{user}{user_posts_count}.{file_extension}'

		legend = request.form['legend']

		my_bucket = get_bucket()
		my_bucket.Object(file.filename).put(Body=file)

		posts = db.get_posts()
		post = {
			'user': user,
			'image': file.filename,
			'text': legend
		}

		posts.append(**post)

	else:
		print('Nenhuma imagem selecionada!')

	return redirect(url_for('user_feed'))
