import logging
import jwt
import time
import datetime
log = logging.getLogger(__name__)

import transaction
from pyramid_mailer.message import Message

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

def send_email(mailer, message):
	message.sender = "upd.ngse.test@gmail.com"
	mailer.send(message)
	transaction.commit()

def send_recommender_email(mailer, applicant_name, recipient, password):
	message = Message(subject="NGSE Recommender Credentials",
		recipients=[recipient],
		body="Good day!\n\n{} has started filling up an application form for the National Graduate School of Engineering and has chosen you to be one of their references. Kindly fill up the form at http://104.198.143.20\n\nThe e-mail to be used when logging in is this e-mail and your generated password is {}".format(applicant_name, password)
		)

	send_email(mailer, message)

def send_credentials_email(mailer, recipient, password):
	message = Message(subject="NGSE Application Credentials",
		recipients=[recipient],
		body="Your generated password is: {}".format(password)
		)

	send_email(mailer, message)

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