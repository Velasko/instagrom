from flask import session, render_template, redirect, url_for

from .. import app
from ..database import database as db
from ..models.forms import PostForm


@app.route("/feed", methods=['GET', 'POST'])
def user_feed():
	form = PostForm()

	posts = db.get_posts()
	likes = db.get_likes()

	if form.validate_on_submit():
		post = {'user': session['username'], 'image': form.content.data}
		posts.append(**post)
		return redirect(url_for('user_feed'))


	return render_template('feed.html', form=form, posts=posts, likes=likes)

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