from database import session
from sqlalchemy.orm.exc import NoResultFound
from models import (
	Base,
	FormType,
	Form,
	Category,
	Question,
	Answer,
	UserType,
	User
)

from utils import JWT_SECRET

import bcrypt
import jwt
import time


def login(request):
	email = request.params['email']
	password = request.params['password']

	user = session.query(User).filter(User.email == email).all()

	error = {
		'message': 'Please check your username or password',
		'success': False
	}

	if (user == []):
		return error
	else:
		user = session.query(User).filter(User.email == email).first()
		pwd = bcrypt.hashpw(password.encode('UTF_8'), user.password.encode('UTF_8'))
		if(pwd == user.password):
			payload = {
				'sub': user.name,
				'exp': int(time.time()) + 60*120,
				'iat': int(time.time()),
				'utype_id': user.user_type_id
			}
			token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
			return {'message' : 'Welcome {}'.format(user.name), 'success': True, 'token': token}
		else:
			return error