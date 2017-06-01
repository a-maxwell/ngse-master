import logging
import jwt
import time
import datetime

import string
import random

log = logging.getLogger(__name__)

import transaction

from pyramid_mailer.message import Message

import random
import string

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

email_template = '<table>\
	<tr>\
		<td rowspan="4"><img src="http://35.184.104.115/static/images/email-logo.png"/></td>\
		<td>\
			<strong>National Graduate School of Engineering</strong><br>\
			College of Engineering<br>\
			UNIVERSITY OF THE PHILIPPINES<br>\
			Diliman, Quezon City 1101 Philippines\
		</td>\
	</tr>\
</table>\
<hr>\
\
{}\
\
<hr>\
<table>\
	<tr><td>ADDRESS</td><td>: Rm. 119-121, Melchor Hall, Osmena Avenue, University of the Philippines, Diliman, Quezon City 1101 Philippines</td></tr>\
	<tr><td>TELEFAX</td><td>: +632-926-0703</td></tr>\
	<tr><td>TRUNKLINE</td><td>: +632-981-8500 local 3105/3106</td></tr>\
	<tr><td>EMAIL</td><td>: ngse@coe.upd.edu.ph</td></tr>\
</table>'

applicant_message = 'Hello, {}.\n\
\n\
Thank you for signing up on our online application form! If you wish to continue with your online application, you may do so anytime. Just login back to our site (http://35.184.104.115/) using the following credentials:\n\
\n\
E-mail: {}\n\
Passcode: {}\n\
\n\
We hope to see you submit your application soon.'

applicant_message_html = 'Hello, {}.<br><br>\
Thank you for signing up on our online application form! If you wish to continue with your online application, you may do so anytime. Just login back to our site (http://35.184.104.115/) using the following credentials:<br><br>\
E-mail: {}<br>\
Passcode: {}<br><br>\
We hope to see you submit your application soon.'

recommender_message = 'Hello, {}.\n\
\n\
{} is applying for the National Graduate School of Engineering and has assigned you to be one of their references of recommendation.\n\
\n\
You may submit your recommendation here via our online form over at our site (http://35.184.104.115/) using the following credentials:\n\
\n\
E-mail: {}\n\
Passcode: {}\n\
\n\
If you have any questions, you may send us an e-mail.\n\
\n\
We hope to see you submit your recommendation soon!'

recommender_message_html = 'Hello, {}.<br><br>\
{} is applying for the National Graduate School of Engineering and has assigned you to be one of their references of recommendation.<br><br>\
You may submit your recommendation here via our online form over at our site (http://35.184.104.115/) using the following credentials:<br><br>\
E-mail: {}<br>\
Passcode: {}<br><br>\
If you have any questions, you may send us an e-mail.<br><br>\
We hope to see you submit your recommendation soon!'

def send_email(mailer, message):
	message.sender = "ngse@coe.upd.edu.ph"
	mailer.send(message)
	transaction.commit()

def send_recommender_email(mailer, name, applicant_name, recipient, password):
	body = recommender_message.format(name, applicant_name, recipient, password)
	html = recommender_message_html.format(name, applicant_name, recipient, password)
	print body
	message = Message(subject="NGSE Online Recommendation",
		recipients=[recipient],
		body=body,
		html=email_template.format(html)
		)

	send_email(mailer, message)

def send_credentials_email(mailer, name, recipient, password):
	body = applicant_message.format(name, recipient, password)
	html = applicant_message_html.format(name, recipient, password)
	print body
	message = Message(subject="NGSE Online Application",
		recipients=[recipient],
		body=body,
		html=email_template.format(html)
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

def password_generator(range_size=8, char_set=string.ascii_uppercase + string.digits+string.ascii_lowercase):
	return ''.join(random.choice(char_set) for _ in range(range_size))
# print id_generator()
