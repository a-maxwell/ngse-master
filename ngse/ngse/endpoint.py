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

def answer_update(request):
	user_id = request.params['user_id']
	q_id = request.params['question_id']
	curr_ans = request.params['answer']

	db_ans = session.query(Answer)\
			.filter(Answer.question_id == q_id)\
			.filter(Answer.user_id == user_id)\
			.all()

	if(db_ans == []):
		try:
			answer = Answer(name=curr_ans, question_id=q_id, user_id=user_id)
			session.add(answer)
			session.commit()
			# return{'message': 'Answer saved', 'success':True}
		except:
			return{'message': 'Smth went wrong', 'success': False}
	else:
		try:
			# update lang here
			answer = session.query(Answer)\
					.filter(Answer.question_id == q_id)\
					.filter(Answer.user_id == user_id)\
					.first()
			answer.name = curr_ans
			session.commit()
			# return{'message': 'Answer saved', 'success':True}
		except:
			return{'message': 'Smth went wrong', 'success':False}
	return{'message': 'Answer saved', 'success':True}

def view_answer(request):
	user_id = request.params['user_id'] #if succesful auth, this should be authenticated_userid(request)
	# form = request.params['form_type']
	try:
		u = session.query(User).filter(User.id == user_id).first()
	except:
		return {'success':False}
	if u == None or u.user_type_id != 3:
		return {'success':False}

	categ=[]
	for item in session.query(Category).filter(Category.form_type_id == 1).all():
		ques_array=[]
		for q in session.query(Question).filter(Question.category_id == item.id).all():
			answer = session.query(Answer.name).filter(Answer.question_id == q.id).filter(Answer.user_id == user_id).first()
			if(answer!=None): answer=answer.name
			ques_array.append({
                # 'category' : item.name,
				'question' : q.name,
				'answer' : answer
			})
		categ.append({
			'name' : item.name,
			'data' : ques_array
			})
		# categ[item.name] = ques_array
	return {'data': categ, 'success': True}

def get_users(request):
	d = []
	for u in session.query(User):
		d.append({
			'id': int(u.id),
			'name': u.name,
			'email': u.email,
			'user_type': u.user_type.name,
			'date_created': str(u.date_created),
			'last_modified': str(u.last_modified)
		})
	return d

def authorize_user(request):
	# check for required params, return error if incomplete

	email = request.params['email']
	password = request.params['password'] # hash this??? huhu di ko pa alam

	# check if email is linked to an account
	try:
		u = session.query(User).filter(User.email == email).one()
	except:
		return {'msg' : 'email not linked to an account', 'success': False}

	# check if user entered correct password
	auth = (u.password == password)

	if not auth:
		# return error message, wrong passcode
		return {'msg': 'invalid email password combination', 'success': False}

	# fetch user type for payload
	user_type = u.user_type.name

	# get jwt and return jwt

	return {
		'auth': auth, 'success': True
	}

	# fetch and return token
	# token = encode()
	# return {'token': token}

def create_user(request):
	# check for required params, return error if incomplete

	email = request.params.get('email', None)
	name = request.params.get('name', None)
	# user_type_id = int(request.params.get('user_type_id', session.query(UserType).filter(UserType.name == 'Applicant').one().id))
	user_type_id = int(request.params.get('user_type_id', 3))

	if email is None or name is None:
		return error(1)

	# check if email is linked to an account
	try:
		u = session.query(User).filter(User.email == email).one()
		return {'msg': 'email is in use', 'success': False}
	except:
		# generate password
		password = bcrypt.hashpw('password', bcrypt.gensalt())

	try:
		u = User(name=name, email=email, password=password)
		session.add(u)
		session.commit()
	except:
		return {'msg': 'an error occured', 'success': False}

	return {'success': True}

def update_user_status(request):
	#if admin
	user_id = request.params['user_id']
	status = request.params['user_status']
	try:
		u = session.query(User).filter(User.id == user_id).first()
	except:
		return {'message': 'Smth went wrong', 'success': False}

	if u == None or user_id == '' or u.user_type_id != 3:
			return {'message': 'Smth went wrong', 'success': False}
	
	u.application_status= status
	session.commit()
	return {'message': 'Status successfully updated', 'success': True}


def view_user_status(request):
	user_id = request.params['user_id']
	try:
		u = session.query(User).filter(User.id == user_id).one()
	except:
		return{'success':False} 
	if (u == None or u.user_type_id != 3):
		return{'success':False} 


	return{'name': u.name, 'Application status': u.application_status, 'success': True}


''' Form views '''

def get_forms(request):
	d = []
	for f in session.query(Form):
		d.append({
			'id': int(f.id),
			'name': f.name
		})
	return d

def create_form(request):
	# we need name, form type id, date start, date end
	name = request.params['name']
	form_type_id = request.params['form_type_id']
	date_start = request.params['date_start']
	date_end = request.params['date_end']

	form = Form(
		name=name,
		date_start=date_start,
		date_end=date_end,
		form_type_id=form_type_id
		)
	session.add(form)
	session.commit()

	return {'success': True}

def delete_form(request):
	id = request.params['id']

	form = session.query(Form)\
	.filter(Form.id == id)\
	.one()

	session.delete(form)
	session.commit()

	return {'success': True}

def show_form(request):
	id = request.params['id']

	try:
		form = session.query(Form)\
			.filter(Form.id == id)\
			.one()
	except:
		return {}

	return form.as_dict()

def update_form(request):
	id = request.params['id']

	form = session.query(Form)\
	.filter(Form.id == id)\
	.one()

	name = request.params.get('name', None)
	if name is not None:
		form.name = name

	date_start = request.params.get('date_start', None)
	if date_start is not None:
		form.date_start = date_start

	date_end = request.params.get('date_end', None)
	if date_end is not None:
		form.date_end = date_end

	form_type_id = request.params.get('form_type_id', None)
	if form_type_id is not None:
		form.form_type_id = form_type_id

	session.commit()

	return form.as_dict()

def list_form_types(request):
	d = []
	for ft in session.query(FormType):
		d.append({
			'id': int(ft.id),
			'name': ft.name,
			'page_sequence': ft.page_sequence,
			'date_created': str(ft.date_created),
			'last_modified': str(ft.last_modified)
		})
	return d