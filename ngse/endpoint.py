from database import session
from sqlalchemy.orm.exc import NoResultFound
from models import (
	Base,
	FormType,
	Form,
	Category,
	Element,
	Answer,
	UserType,
	User,
	form_category_association,
	ApplicantAttribute
)

from utils import encode, decode, log, generateError, generateSuccess, generateToken, is_past

import bcrypt


'''users'''

def show_user(request):
	_id = request.params['id']

	user = session.query(User)\
		.filter(User.id == _id)\
		.one()

	d = {
		'name': user.name,
		'date_created': str(user.date_created),
		'last_modified': str(user.last_modified),
		'email': user.email,
		'user_type_id': user.user_type_id
	}

	if (user.user_type_id in [4,5]):
		d['application_status'] = user.application_status

	if (user.user_type_id in [3,4,5]):
		answers = session.query(Answer)\
			.filter(Answer.user_id == id)\
			.all()

		d['answers'] = []

		for answer in answers:
			d['answers'].append({
				'id': answer.id,
				'question_id': answer.question_id,
				'name': answer.name
			})

	return d














################################################################

def get_forms(request):
	d = []
	for f in session.query(Form):
		started = is_past(str(f.date_start))
		ended = is_past(str(f.date_end))

		status = 'idle' if (not started) else ( 'expired' if (ended) else 'ongoing' )

		d.append({
			'id': int(f.id),
			'name': f.name,
			'user': f.form_type.user_type_id,
			'date_start': str(f.date_start),
			'date_end': str(f.date_end),
			'status': status
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
	_id = request.params['id']

	form = session.query(Form)\
	.filter(Form.id == _id)\
	.one()

	session.delete(form)
	session.commit()

	return {'success': True}

def show_form(request):
	form_id = request.params['form_id']

	try:
		form = session.query(Form)\
			.filter(Form.id == form_id)\
			.one()
	except:
		return generateError('Invalid form id')

	d = {
		'name': form.name,
		'date_created': str(form.date_created),
		'last_modified': str(form.last_modified),
		'date_start': str(form.date_start),
		'date_end': str(form.date_end),
		'form_type_id': form.form_type_id,
		'user_type_id': form.form_type.user_type_id,
		'page_sequence': form.form_type.page_sequence
	}

	return d

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

	return generateSuccess('Success')

def get_form_types(request):
	d = []
	for ft in session.query(FormType):
		d.append({
			'id': ft.id,
			'name': ft.name,
			'page_sequence': ft.page_sequence,
			'date_created': str(ft.date_created),
			'last_modified': str(ft.last_modified)
		})
	return d

################################################################

def get_categories(request):
	form_id = request.params.get('form_id')

	form = session.query(Form)\
		.filter(Form.id == form_id)\
		.one()

	result = []

	for category in session.query(Category).join(Category.form_type, aliased=True).filter_by(id = form.form_type_id):
		result.append({
			'id': category.id,
			'name': category.name
		})

	return result

def show_category(request):
	category_id = request.params.get('category_id')

	category = session.query(Category)\
		.filter(Category.id == category_id)\
		.one()

	d = {
		'id': category.id,
		'name': category.name,
		'date_created': str(category.date_created),
		'last_modified': str(category.last_modified),
		'form_type_ids': []
	}

	associations = session.query(form_category_association)\
		.filter(form_category_association.c.categories_id == category.id)\
		.all()

	for association in associations:
		d['form_type_ids'].append(association.form_types_id)

	return d



################################################################


def get_questions(request):
	category_id = request.params.get('category_id')
	result = []

	for question in session.query(Element).filter(Element.category_id == category_id):
		q = {
			'id': int(question.id),
			'name': question.name,
			'input_type': question.input_type
		}

		if (question.choices):
			q['choices'] = choices
		
		result.append(q)

	return result

################################################################

def get_answers(request):
	user_id = request.params.get('user_id')
	category_id = request.params.get('category_id')
	result = []

	for answer in session.query(Answer).filter(Answer.user_id == user_id).join(Answer.question, aliased=True).filter_by(category_id=category_id):
		result.append({
			'id': answer.id,
			'name': answer.name,
			'question_id': answer.question_id
		})
	
	return result

def update_answer(request):
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
		for q in session.query(Element).filter(Element.category_id == item.id).all():
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

	if token is None:
		return generateError('Token is missing', {'expired': False})

	try:
		payload = decode(token)
	except jwt.ExpiredSignatureError:
		return generateError('Token has expired', {'expired': True})
	except:
		return generateError('Token is invalid', {'expired': False})

	return generateSuccess('Token is valid', {'expired': False})

def login_user(request):
	email = request.params.get('email', None)
	password = request.params.get('password', None)

	print request.POST

	if email is None or password is None:
		return generateError('Invalid email/password')

	try:
		user = session.query(User).filter(User.email == email).one()
	except NoResultFound:
		return generateError('Invalid email')

	pwd = bcrypt.hashpw(password.encode('UTF_8'), user.password.encode('UTF_8'))

	if (pwd != user.password):
		return generateError('Invalid password')

	return generateSuccess('Welcome, {}!'.format(user.name), {'token': generateToken(user)})

def create_user(request):
	# check for required params, return error if incomplete

	email = request.params.get('email', None)
	last = request.params.get('last', None)
	given = request.params.get('given', None)
	middlemaiden = request.params.get('middlemaiden', None)
	level = request.params.get('level', None)
	fullname = '{} {}'.format(given, last)
	password = bcrypt.hashpw('password', bcrypt.gensalt())

	if email is None or last is None or given is None or middlemaiden is None:
		return generateError('Field is missing')

	# check if user is not recommender email is linked to an account
	u = session.query(User).filter(User.email == email).all()
	if (level != 3 and len(u) > 0):
		return generateError('E-mail is already in use')

	try:
		if level is None:
			u = User(name=fullname, email=email, password=password)
		else:
			u = User(name=fullname, email=email, password=password, user_type_id=int(level))
	except:
		return generateError('Something weird happened!')

	session.add(u)
	session.commit()

	if int(level) in [4,5]:

		print 'HUH'
		# create answer} 
		form_type = session.query(FormType).filter(FormType.user_type_id == u.user_type_id).one()
		# forms = session.query(Form).filter(Form.form_type_id == form_type.id).all()
		# for f in forms:
		# 	started = is_past(str(f.date_start))
		# 	ended = is_past(str(f.date_end))

		# 	status = 'idle' if (not started) else ( 'expired' if (ended) else 'ongoing' )

		# 	if (status is 'ongoing'):
		# 		form = f
		# 		break
		category_ids = form_type.page_sequence
		questions = []

		for category_id in category_ids:
			toadd = session.query(Element).filter(Element.klass == 'question').filter(Element.category_id == category_id).all()
			for entry in toadd:
				questions.append(entry)

		for question in questions:
			answer = Answer(text='', element_id=question.id, user_id=u.id)
			session.add(answer)
			session.commit()

	return generateSuccess('Welcome, {}!'.format(fullname), {'token': generateToken(u)})

def delete_user(request):
	'''
	input id of user accessing endpoint, id of user to delete, type of user
	input step number for testing
	'''

	step = int(request.params.get('step', 0)) # variable for testing
	user_id = request.params.get('user_id', None)
	_id = request.params.get('id', None)

	if user_id is None or _id is None: # user_id was not passed
		return generateError('Required field is missing')

	try:
		user_id = int(user_id)
	except ValueError: # user_id not an integer
		return generateError('user_id is invalid')

	if user_id < 1 or user_id > 2147483647: # user_id beyond range
		return generateError('user_id is out of bounds')

	try:
		_id = int(_id)
	except ValueError: # id not an integer
		return generateError('id is invalid')

	if _id < 1 or _id > 2147483647:
		return generateError('id is out of bounds')

	try:
		user = session.query(User).filter(User.id == user_id).one()
	except NoResultFound: # user_id not found in database 
		return generateError('User accessing does not exist')

	user_type = user.user_type_id

	if ((user_type != 1) and (user_id != _id)): # not admin deleting different id
		return generateError('Unauthorized')

	if ((user_type == 1) and (user_id == _id)): # admin deleting admin id
		return generateError('Cannot delete admin account')

	try:
		other_user = session.query(User).filter(User.id == _id).one()
	except NoResultFound: # id not found in database
		return generateError('User ')

	if step == 5:
		return {'message': 'other user exists'}


	# return {'message': 'oh no', 'success': False}

def update_application_status(request):
	#if admin
	user_id = request.params['user_id']
	status = request.params['a_status']

	app = session.query(ApplicantAttribute).filter(ApplicantAttribute.applicant_id == user_id).first()

	if app == None: return{'message': 'user is not an applicant', 'success':False}
	app.application_status= status
	session.commit()
	return {'message': 'Status successfully updated', 'success': True}


#returns application and validation status of applicant
def view_status(request): 
	user_id = request.params['user_id']
	app = session.query(ApplicantAttribute).filter(ApplicantAttribute.applicant_id == user_id).first()

	if app == None: return{'message': 'user is not an applicant', 'success':False}
	user = session.query(User).filter(User.id == user_id).first()					

	return{ 'name': user.name, 'application status': app.application_status, 'validation_status': app.validation_status}

def update_validation_status(request):
	user_id = request.params['user_id']
	status = request.params['v_status'] # complete, incomplete, not yet submitted
	app = session.query(ApplicantAttribute).filter(ApplicantAttribute.applicant_id == user_id).first()
	
	if app == None: return{'message': 'user is not an applicant', 'success':False}
	app.validation_status= status
	session.commit()
	return {'message': 'Validation status successfully updated', 'success': True}


def reset_database(request):
	# if admin

	# problem: does not delete the id sequence
	session.query(Answer).delete()
	session.commit()
	session.query(ApplicantAttribute).delete()
	session.commit()
	users = session.query(User).filter(User.id > 1).all()
	for user in users:
		session.delete(user)
		session.commit()
	return {'success': True}

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