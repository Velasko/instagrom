import flask
import flask_login
from .filters import datetimeformat

app = flask.Flask(__name__)

#generating a new secret key:
#python -c 'import os; print(os.urandom(16))'
app.secret_key = b'\xc4>#\xa1E\x1e\xa0a1\x93\xbe?s\xea\xbf\xf1'
app.jinja_env.filters['datetimeformat'] = datetimeformat

login_manager = flask_login.LoginManager()
login_manager.init_app(app)
