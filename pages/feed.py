from flask import session, render_template, redirect, url_for

from .. import app
from ..database import database as db
from ..models.forms import PostForm


@app.route("/feed", methods=['GET', 'POST'])
def user_feed():
	form = PostForm()

	posts = db.get_posts()

	if form.validate_on_submit():
		post = {'user': session['username'], 'image': form.content.data}
		posts.append(**post)
		return redirect(url_for('user_feed'))


	return render_template('feed.html', form=form, posts=posts)