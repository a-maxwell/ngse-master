from database import session
from sqlalchemy.orm.exc import (NoResultFound, MultipleResultsFound)
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
	ApplicantAttribute,
	CategoryStatus
)

from utils import encode, decode, log, generateError, generateSuccess, generateToken, is_past, word

import bcrypt


'''users'''

from sqlalchemy import func
def show_user(request):
	user_id = request.params['user_id']

	user = session.query(User)\
		.filter(User.id == user_id)\
		.one()

	d = {
		'name': user.name,
		'date_created': str(user.date_created),
		'last_modified': str(user.last_modified),
		'email': user.email,
		'user_type_id': user.user_type_id
	}


	if (user.user_type_id in [4,5]):
		# d['application_status'] = user.application_status
		attrib = session.query(ApplicantAttribute).filter(ApplicantAttribute.applicant_id==user_id).one()
		d['validation_status'] = attrib.validation_status
		d['application_status'] = attrib.application_status
		d['answered_pos'] = attrib.answered_pos

		d['level'] = attrib.level
		d['program'] = attrib.program
		d['program_type'] = attrib.program_type
		d['student_type'] = attrib.student_type
		d['choice_1'] = attrib.choice_1
		d['choice_2'] = attrib.choice_2
		d['choice_3'] = attrib.choice_3
		d['adviser'] = attrib.adviser
		d['start_of_study'] = attrib.start_of_study
		d['year'] = attrib.year
		d['other_scholarship'] = attrib.other_scholarship
		d['other_scholarship_name'] = attrib.other_scholarship_name

		# get recommender statuses
		if (attrib.recommender_a == None):
			d['recommender_a_status'] = 'Unassigned'
		else:
			d['recommender_a_status'] = 'Submitted'
			category_statuses = session.query(CategoryStatus)\
				.filter(CategoryStatus.user_id == attrib.recommender_a)\
				.all()
			for category_status in category_statuses:
				print category_status
				if category_status.status is False:
					d['recommender_a_status'] = 'Not yet finished'

		if (attrib.recommender_b == None):
			d['recommender_b_status'] = 'Unassigned'
		else:
			d['recommender_b_status'] = 'Submitted'
			category_statuses = session.query(CategoryStatus)\
				.filter(CategoryStatus.user_id == attrib.recommender_b)\
				.all()
			for category_status in category_statuses:
				if category_status.status is False:
					d['recommender_b_status'] = 'Not yet finished'

		if (attrib.recommender_c == None):
			d['recommender_c_status'] = 'Unassigned'
		else:
			d['recommender_c_status'] = 'Submitted'
			category_statuses = session.query(CategoryStatus)\
				.filter(CategoryStatus.user_id == attrib.recommender_c)\
				.all()
			for category_status in category_statuses:
				if category_status.status is False:
					d['recommender_c_status'] = 'Not yet finished'


	if (user.user_type_id in [3,4,5]):
		categories = session.query(CategoryStatus)\
			.filter(CategoryStatus.user_id == user_id)\
			.all()

		d['answered'] = []

		for category in categories:
			d['answered'].append({
				'id': category.id,
				'category_id': category.category_id,
				'status': category.status	
			})

		answers = session.query(Answer)\
			.filter(Answer.user_id == user_id)\
			.all()

		d['answers'] = []

		for answer in answers:
			d['answers'].append({
				'id': answer.id,
				'category_id': answer.element.category_id,
				'element_id': answer.element_id,
				'name': answer.text
			})

	return d

def update_user(request):
	token = request.authorization[1]
	payload = decode(token)
	user_id = payload['sub']

	user = session.query(User)\
		.filter(User.id == user_id)\
		.one()

	user_attribs = session.query(ApplicantAttribute)\
		.filter(ApplicantAttribute.applicant_id == user_id)\
		.one()

	attribs = [
		'level',
		'program',
		'program_type',
		'student_type',
		'choice_1',
		'choice_2',
		'choice_3',
		'adviser',
		'start_of_study',
		'year',
		'other_scholarship',
		'other_scholarship_name'
	]

	for key in attribs:
		value = request.params.get('user[{}]'.format(key))
		if (key == 'level'):
			user_attribs.level = value
		if (key == 'program'):
			user_attribs.program = value
		if (key == 'program_type'):
			user_attribs.program_type = value
		if (key == 'student_type'):
			user_attribs.student_type = value
		if (key == 'choice_1'):
			user_attribs.choice_1 = value
		if (key == 'choice_2'):
			user_attribs.choice_2 = value
		if (key == 'choice_3'):
			user_attribs.choice_3 = value
		if (key == 'adviser'):
			user_attribs.adviser = value
		if (key == 'start_of_study'):
			user_attribs.start_of_study = value
		if (key == 'year'):
			user_attribs.year = value
		if (key == 'other_scholarship'):
			user_attribs.other_scholarship = value
		if (key == 'other_scholarship_name'):
			user_attribs.other_scholarship_name = value

	user_attribs.answered_pos = True

	session.commit()

	return {'success': True}










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


def get_elements(request):
	category_id = request.params.get('category_id')
	result = []

	for element in session.query(Element).filter(Element.category_id == category_id):
		q = {
			'id': int(element.id),
			'name': element.name,
			'text': element.text,
			'klass': element.klass,
			'kind': element.kind,
			'width': word(element.width)
		}
 
		if (element.klass == 'question'):
			q['required'] = element.required

		if (element.choices):
			q['choices'] = element.choices

		if (element.default):
			q['default'] = element.default
		
		result.append(q)

	return result

################################################################

# def get_answers(request): # old
# 	user_id = request.params.get('user_id')
# 	category_id = request.params.get('category_id')
# 	result = []

# 	for answer in session.query(Answer).filter(Answer.user_id == user_id).join(Answer.element, aliased=True).filter_by(category_id=category_id):
# 		result.append({
# 			'id': answer.id,
# 			'text': answer.text,
# 			'element_id': answer.element_id
# 		})
	
# 	return result

def get_answers(request): # new
	result = []

	for answer in session.query(Answer):
		result.append({
			'id': answer.id,
			'text': answer.text,
			'element_id': answer.element_id,
			'user_id': answer.user_id
		})
	
	return result

def update_answer(request):
	user_id = request.params.get('user_id')
	category_id = request.params.get('category_id')
	data = request.params.get('data')
	length = request.params.get('length')

	# change category status to answered
	category_status = session.query(CategoryStatus)\
		.filter(CategoryStatus.user_id == user_id)\
		.filter(CategoryStatus.category_id == category_id)\
		.one()

	category_status.status = True
	session.commit()

	for i in range(int(length)):
		answer_id = request.params.get('data[{}][id]'.format(i))
		text = request.params.get('data[{}][text]'.format(i))
		
		answer = session.query(Answer)\
			.filter(Answer.user_id == user_id)\
			.filter(Answer.id == answer_id)\
			.one()
		answer.text = text
	
		e = session.query(Element).filter(Element.id == answer.element_id).one()
		# if answer.element_id in [70, 71, 75, 76, 80, 81] and text != '':
		if (e.text == "Recommender Name" or e.text == "Recommender E-mail" ) and (text != ""):	
			# if hindi pa existing create a new recommender
			# if answer.element_id in [70, 75, 80]:
			if e.text == "Recommender Name":
				recName = text;

			# elif answer.element_id in [71, 76, 81]:
			elif e.text == "Recommender E-mail":
				attr = session.query(ApplicantAttribute)\
					.filter(ApplicantAttribute.applicant_id == user_id).one()

				password = bcrypt.hashpw('password', bcrypt.gensalt())
				# EDIT: FIX THE EMAIL PART

				rec = User(name=recName, email=text, password=password, user_type_id='3')
				# session.add(rec)
				# session.commit()

				print answer.element_id
				success = False

				# if answer.element_id == 71 and attr.recommender_a == None:
				if e.name == "rec1email" and attr.recommender_a == None:	
					session.add(rec)
					session.commit()
					attr.recommender_a = rec.id
					session.commit()
					success = True
				# elif answer.element_id == 76 and attr.recommender_b == None:
				elif e.name == "rec2email" and attr.recommender_b == None:
					session.add(rec)
					session.commit()
					attr.recommender_b = rec.id
					session.commit()
					success = True
				# elif answer.element_id == 81 and attr.recommender_c == None:
				elif e.name == "rec3email" and attr.recommender_c == None:				
					session.add(rec)
					session.commit()
					attr.recommender_c = rec.id
					session.commit()
					success = True
				if(success):
					form_type = session.query(FormType).filter(FormType.user_type_id == rec.user_type_id).one()
					category_ids = form_type.page_sequence
					questions = []
					for category_id in category_ids:
						toadd = session.query(Element).filter(Element.klass == 'question').filter(Element.category_id == category_id).all()
						for entry in toadd:
							questions.append(entry)

					for question in questions:
						answer = Answer(text='', element_id=question.id, user_id=rec.id)
						session.add(answer)
						session.commit()			

		########
	session.commit()
	return generateSuccess('Successfully updated answer')




	# db_ans = session.query(Answer)\
	# 		.filter(Answer.element_id == q_id)\
	# 		.filter(Answer.user_id == user_id)\
	# 		.all()

	# if(db_ans == []):
	# 	try:
	# 		answer = Answer(name=curr_ans, element_id=q_id, user_id=user_id)
	# 		session.add(answer)
	# 		session.commit()
	# 		# return{'message': 'Answer saved', 'success':True}
	# 	except:
	# 		return{'message': 'Smth went wrong', 'success': False}
	# else:
	# 	try:
	# 		# update lang here
	# 		answer = session.query(Answer)\
	# 				.filter(Answer.element_id == q_id)\
	# 				.filter(Answer.user_id == user_id)\
	# 				.first()
	# 		answer.name = curr_ans
	# 		session.commit()
	# 		# return{'message': 'Answer saved', 'success':True}
	# 	except:
	# 		return{'message': 'Smth went wrong', 'success':False}
	# return{'message': 'Answer saved', 'success':True}

# def view_answer(request):
def show_answer(request):
	user_id = request.params['user_id']
	category_id = request.params['category_id']

	result = []

	for answer in session.query(Answer).filter(Answer.user_id == user_id).join(Answer.element, aliased=True).filter_by(category_id=category_id):
		result.append({
			'id': answer.id,
			'text': answer.text,
			'date_created': str(answer.date_created),
			'last_modifed': str(answer.last_modified),
			'element_id': answer.element_id
		})

	return result

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

	if email is None or password is None:
		return generateError('Invalid email and password combination')

	try:
		user = session.query(User).filter(User.email == email).one()
		pwd = bcrypt.hashpw(password.encode('UTF_8'), user.password.encode('UTF_8'))

		if (pwd != user.password):
			return generateError('Invalid email and password combination')
	except MultipleResultsFound:
		users = session.query(User).filter(User.email == email).all()
		user = None
		for u in users:
			pwd = bcrypt.hashpw(password.encode('UTF_8'), u.password.encode('UTF_8'))
			if (pwd == u.password):
				user = u
				break
		if user == None:  
			return generateError('Invalid email and password combination')

	except NoResultFound:
		return generateError('Invalid email and password combination')


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

	if int(level) in [3,4,5]:

		#######
		# add a row in ApplicantAttribute Table
		if level == '4':
			row = ApplicantAttribute(scholarship = False, applicant_id=u.id)
		elif level == '5':
			row = ApplicantAttribute(scholarship = True, applicant_id=u.id)
		
		if int(level) in [4,5]:
			session.add(row)
			session.commit()
		#######

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
			if question.default:
				answer.text = question.default
			session.add(answer)
			session.commit()

		# initialize all status of categories_answered to False
		for category_id in category_ids:
			category_status = CategoryStatus(user_id=u.id, category_id=category_id)
			session.add(category_status)

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
''' edit: this is already in show_user function
def view_status(request): 
	user_id = request.params['user_id']
	app = session.query(ApplicantAttribute).filter(ApplicantAttribute.applicant_id == user_id).first()

	if app == None: return{'message': 'user is not an applicant', 'success':False}
	user = session.query(User).filter(User.id == user_id).first()					

	return{ 'name': user.name, 'application status': app.application_status, 'validation_status': app.validation_status}
'''
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
# 	return {'success': True}