import os
import flask
import flask_login
from .filters import datetimeformat

from flask_dynamo import Dynamo

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = __file__[:21] + os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

app = flask.Flask(__name__)

app.config['DYNAMO_TABLES'] = [
	{
		'TableName':'Likes',
		'keySchema':[
			dict(AttributeName='user', KeyType='String'),
			dict(AttributeName='post', KeyType='Number')
		],
		'AttributeDefinitions':[
			dict(AttributeName='user', AttributeType='S'),
			dict(AttributeName='post', AttributeType='S')
		],
		'ProvisionedThroughput':dict(ReadCapacityUnits=5, WriteCapacityUnits=5)
	}
]

dynamo = Dynamo(app)
dynamo.init_app(app)

#generating a new secret key:
#python -c 'import os; print(os.urandom(16))'
app.secret_key = os.getenv('FLASK_SECRET_KEY')
app.jinja_env.filters['datetimeformat'] = datetimeformat

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

from . import pages

#if __name__ == 'instagrom':
#	app.run()