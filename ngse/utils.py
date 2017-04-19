import logging
import jwt
import time
import datetime
log = logging.getLogger(__name__)

JWT_SECRET = "NationalGraduateSchoolOfEng'g"

URI = {
	# resources
	'users': '/users',
	'recommenders': '/recommenders',
	'forms': '/forms',
	'categories': '/categories',
	'questions': '/questions',
	'elements': '/elements',
	'answers': '/answers',
	# actions
	'verify': '/verify',
	'login': '/login',
	'create': '/create',
	'delete': '/delete',
	'search': '/search',
	'show': '/show',
	'types': '/types',
	'update': '/update',
	'validate': '/validate'
}

def is_past(date):
	return datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S') < datetime.datetime.now()

def encapsulate(primary, secondary='', action='', base='/v1'):
	return base+primary+secondary+action

def encode(payload):
	return jwt.encode(payload, JWT_SECRET, algorithm='HS256')

def decode(token):
	return jwt.decode(token, JWT_SECRET)

def generateError(message, extra_fields=None):
	d = {'success': False, 'message': message}
	if extra_fields is not None:
		d.update(extra_fields)
	return d

def generateSuccess(message, extra_fields=None):
	d = {'success': True, 'message': message}
	if extra_fields is not None:
		d.update(extra_fields)
	return d

def generateToken(user):
	current_time = int(time.time())
	expiry_time = current_time + 60*120

	payload = {
		'sub': user.id,
		'exp': expiry_time,
		'iat': current_time,
		'name': user.name,
		'level': user.user_type_id
	}

	token = encode(payload)

	return token

def word(n):
	if int(n) < 1:
		n = 1

	if int(n) > 16:
		n = 16

	words = [
		'zero',
		'one',
		'two',
		'three',
		'four',
		'five',
		'six',
		'seven',
		'eight',
		'nine',
		'ten',
		'eleven',
		'twelve',
		'thirteen',
		'fourteen',
		'fifteen',
		'sixteen'
	]

	return words[n]