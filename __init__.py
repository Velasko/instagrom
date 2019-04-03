import flask
import flask_login

from flask_dynamo import Dynamo

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
app.secret_key = b'\xc4>#\xa1E\x1e\xa0a1\x93\xbe?s\xea\xbf\xf1'

login_manager = flask_login.LoginManager()
login_manager.init_app(app)
