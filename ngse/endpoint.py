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

def error(message):
	return {'success': False, 'message': message}

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
'''
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
			if(answer!=None): 
				answer=answer.name
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
'''


def view_answer(request):
	# 1
	user_id = request.params['user_id']
	# return {'id':user_id}
	# 2
	try:
		u = session.query(User).filter(User.id == user_id).first()
		# return {'u_name':u.name}
	except:
		# 3
		return{'success':False}
		# pass
	# 4
	# if u.user_type_id != 3: 
	# 	return{'success': False}
	# return{'success': True}
	
	# 5
	# if u.user_type_id != 3: 
	# 	return{'success': False}
	# return{'success': True}
	if u == None or u.user_type_id != 3:
		return{'success': False}
	# 6
	categ=[]
	# return {'list': categ}
	
	c = 0; #for debugging and testing lang this 
	# 7
	for item in session.query(Category).filter(Category.form_type_id == 1).all():
		# print item.name
		# c+=1
		# if c == 9:
		# 	return{'categ': item.name}
		# 8
		ques_array=[]
		# return {'list': ques_array}
		# 9
		for q in session.query(Question).filter(Question.category_id == item.id).all():
			c+=1 #for debugging and testing purposes
			# print q.name, c
			 
			# 	return {'q': q.name} #Last Name, Overall Evaluation
			# 10
			answer = session.query(Answer.name).filter(Answer.question_id == q.id).filter(Answer.user_id == user_id).first()
			# if c == 78:
			# 	return {'name': answer.name}
			# if q.id == 4:
			# 11
			if(answer!=None):
				# 12
				answer=answer.name
			# 13
			ques_array.append({
				'question' : q.name,
				'answer' : answer
			})
			# if  q.id == 3:
			# 	return {'q_array': ques_array}
		# 14
		categ.append({
			'name' : item.name,
			'data' : ques_array
			})
		# if item.id == 2: #last categ id 
		# 	return {'categ': categ}
	# 15
	return {'data': categ, 'success': True}
				
			

# return{'categ': item.name}

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

def verify_user(request):
	token = request.params.get('token', None)
	level = request.params.get('level', 10)

	if token is None:
		return {'message': 'Token is missing', 'expired': False, 'success': False}

	try:
		payload = jwt.decode(token, JWT_SECRET)
	except jwt.ExpiredSignatureError:
		return {'message': 'Token has expired', 'expired': True, 'success': False}

	if payload['level'] > level:
		return {'message': 'Access denied', 'expired': False, 'success': False}

	return {'message': 'Access granted', 'expired': False, 'success': True}

def login_user(request):
	email = request.params.get('email', None)
	password = request.params.get('password', None)

	error = {
		'message': 'Invalid email/password',
		'success': False
	}

	if email is None or password is None:
		error['step'] = 1
		return error

	try:
		user = session.query(User).filter(User.email == email).one()
	except NoResultFound:
		error['step'] = 2
		return error

	pwd = bcrypt.hashpw(password.encode('UTF_8'), user.password.encode('UTF_8'))

	if (pwd != user.password):
		error['step'] = 3
		return error

	current_time = int(time.time())
	expiry_time = current_time + 60*120

	payload = {
		'sub': user.name,
		'exp': expiry_time,
		'iat': current_time,
		'level': user.user_type_id
	}
	token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
	return {'message' : 'Welcome, {}!'.format(user.name), 'success': True, 'token': token}

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

def delete_user(request):

	'''
	
	input id of user accessing endpoint, id of user to delete, type of user
	input step number for testing

	'''

	# variable for testing
	step = int(request.params.get('step', 0))

	'''user_id testing'''

	user_id = request.params.get('user_id', None)

	# user_id was not passed
	if user_id is None:
		return {'message': 'user_id is missing'}

	# test if user_id value is integer
	try:
		int(user_id)
	except ValueError:
		return {'message': 'user_id is invalid'}

	if int(user_id) < 1:
		return {'message': 'user_id must not be less than 1'}

	if int(user_id) > 2147483647:
		return {'message': 'user_id is too large'}

	if step == 1:
		return {'message': 'user_id is valid'}

	'''id testing'''
	_id = request.params.get('id', None)

	# user_id was not passed
	if _id is None:
		return {'message': 'id is missing'}

	# test if user_id value is integer
	try:
		int(_id)
	except ValueError:
		return {'message': 'id is invalid'}

	if int(_id) < 1:
		return {'message': 'id must not be less than 1'}

	if int(_id) > 2147483647:
		return {'message': 'id is too large'}

	if step == 2:
		return {'message': 'id is valid'}

	'''user entry in database testing'''
	try:
		user = session.query(User).filter(User.id == user_id).one()
	except NoResultFound:
		return {'message': 'user does not exist'}

	if step == 3:
		return {'message': 'user exists'}

	'''accessibility testing'''
	user_type = user.user_type_id

	if user_type != 1:
		if user_id == _id:
			if step == 4:
				return {'message': 'user not admin but same id'}
		else:
			return {'message': 'user not admin but diff id'}
	else:
		if user_id == _id:
			return {'message': 'admin trying to delete admin account'}
		else:
			if step == 4:
				return {'message': 'admin trying to delete other account'}

	try:
		other_user = session.query(User).filter(User.id == _id).one()
	except NoResultFound:
		return {'message': 'other user does not exist'}

	if step == 5:
		return {'message': 'other user exists'}


	# return {'message': 'oh no', 'success': False}

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