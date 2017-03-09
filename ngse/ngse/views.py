from cornice import Service
import json
import sqlalchemy

from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget
from pyramid.security import authenticated_userid
from pyramid.security import unauthenticated_userid
from pyramid.security import (
    Authenticated,
    Everyone,
	Allow
)
import bcrypt
import jwt
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from models import (
	Base,
	FormType,
	Form,
	Category,
	Question,
	Answer,
	UserType,
	User,
	# ApplicantAttribute
)
from utils import connect, encapsulate, URI, log #, error #wat error
from setup import setup


def create_resource(resource, primary, secondary='', extra=[]):
	d = {
		'collection': Service(name=resource, path=encapsulate(primary, secondary), renderer='json', description="Fetch list of {}".format(resource)),
		'actions': {
			'create': Service(name='create {}'.format(resource), path=encapsulate(primary, secondary, URI['create']), renderer='json', description="Create {}".format(resource)),
			'delete': Service(name='delete {}'.format(resource), path=encapsulate(primary, secondary, URI['delete']), renderer='json', description="Delete {}".format(resource)),
			'show': Service(name='show {}'.format(resource), path=encapsulate(primary, secondary, URI['show']), renderer='json', description="Show {} information".format(resource)),
			'update': Service(name='update {}'.format(resource), path=encapsulate(primary, secondary, URI['update']), renderer='json', description="Update {} information".format(resource))
		}
	}

	for item in extra:
		key = item['key']
		name = item['name']
		desc = item['description']
		d['actions'][key] = Service(name=name, path=encapsulate(primary, secondary, URI[key]), renderer='json', description=desc)

	return d

user = create_resource("user", URI['users'],
	extra=[
		{
			'key': 'authorize',
			'name': 'authorize user',
			'description': 'Return JWT upon successful authorization'
		},
		{
			'key': 'search',
			'name': 'search user',
			'description': 'Search for set of users'
		},
		{
			'key': 'types',
			'name': 'list user types',
			'description': 'List all types of users'
		},
		{
			'key': 'validate',
			'name': 'validate user',
			'description': 'Validate the status of the user'
		}
	])
# user['actions']['authorize'] = Service(name='authorize user', path=encapsulate(URI['users'], URI['authorize']), description="Return JWT upon successful authorization")
# user['actions']['search'] = Service(name='search user', path=encapsulate(URI['users'], URI['search']), description="Search for set of users")
# user['actions']['types'] = Service(name='list user types', path=encapsulate(URI['users'], URI['types']), description="List all types of users")
# user['actions']['validate'] = Service(name='validate user', path=encapsulate(URI['users'], URI['validate']), description="Validate the status of the user")

user_collection = user['collection']
user_authorize = user['actions']['authorize']
user_create = user['actions']['create']
user_delete = user['actions']['delete']
user_search = user['actions']['search']
user_show = user['actions']['show']
user_types = user['actions']['types']
user_update = user['actions']['update']
user_validate = user['actions']['validate']

recommender = create_resource("recommender", URI['users'], URI['recommenders'])

recommender_collection = recommender['collection']
recommender_create = recommender['actions']['create']
recommender_delete = recommender['actions']['delete']
recommender_show = recommender['actions']['show']
recommender_update = recommender['actions']['update']

form = create_resource("form", URI['forms'])

form_collection = form['collection']
form_create = form['actions']['create']
form_delete = form['actions']['delete']
form_show = form['actions']['show']
form_update = form['actions']['update']

category = create_resource("category", URI['forms'], URI['categories'])

category_collection = category['collection']
category_create = category['actions']['create']
category_delete = category['actions']['delete']
category_show = category['actions']['show']
category_update = category['actions']['update']

question = create_resource("question", URI['forms'], URI['questions'])

question_collection = question['collection']
question_create = question['actions']['create']
question_delete = question['actions']['delete']
question_show = question['actions']['show']
question_update = question['actions']['update']

''' Database setup '''

if 'TRAVIS' in  os.environ:
	db, engine, meta = connect('postgres', '', 'ngsewebsite')
else:
	db, engine, meta = connect('ngse', 'ngse', 'ngsewebsite')
Base.metadata.create_all(engine)
SessionFactory = sessionmaker(engine)
session = SessionFactory()
setup(session)

''' User views '''
login_url = '/v1/login'
answers_url = '/v1/users/answers'
update_answer_url = 'v1/users/update_answer'
user_login = Service(name='user_login', path=login_url, description="logging in")
# user_logout = Service(name='user_logout', path=logout_url, description="logging out")
view_answers = Service(name='view_answers', path=answers_url, description="view answers")
update_answer = Service(name='update_answer', path=update_answer_url, description="update answer")
# __acl__ = 	[(Allow, Everyone, 'view'),
#  		# 	 (Allow, Authenticated, 'auth')
#             ]

def is_authenticated(request):
	#returns null if not logged in
	#else returns id of loged in user
	return authenticated_userid(request)

@user_login.get()
def login(request):
	email = request.params['email']
	password = request.params['password']

	user = session.query(User).filter(User.email == email).all()

	if (user == []):
		return {'message': 'Please check your username or password', 'success': False}
	else:
		user = session.query(User).filter(User.email == email).first()
		pwd = bcrypt.hashpw(password.encode('UTF_8'), user.password.encode('UTF_8'))
		if(pwd == user.password):
			return {'message' : 'Welcome', 'success': True}
		else:
			return {'message': 'Please check your username or password', 'success': False}


@update_answer.get()
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



@view_answers.get()
def view_answer(request):
	user_id = request.params['user_id'] #if succesful auth, this should be authenticated_userid(request)
	# form = request.params['form_type']
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
	return categ

'''
@view_status.get()
def user_status(request):
	user_id = request.params['user_id']
	u = session.query(User).filter(User.id == user_id).first()
	return{'name': u.name, 'Application status': u.status}
'''

@user_collection.get()
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

@user_authorize.post()
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

@user_create.post()
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
		password = 'password'

	try:
		u = User(name=name, email=email, password=password)
		session.add(u)
		session.commit()
	except:
		return {'msg': 'an error occured', 'success': False}

	return {'success': True}

@user_delete.get()
def delete_user(request):
	'''
	if admin: proceed
	else: forbidden
	'''
	#assuming  muna na admin yung logged in
	user_id = request.params['id']
	user = session.query(User).filter(User.id == user_id).one()
	session.delete(user)
	session.commit()
	return {'msg':'user deleted', 'success': True}

@user_search.get()
def search_user(request):
	log.debug('{}'.format(request.params))
	return {'hello': 'yes'}

@user_show.get()
def show_user(request):
	'''
	if admin: proceed
	else:
		if param user id and token user id are the same:
			proceed
		else:
			not authorized
	'''
	return {'hello': 'yes'}

@user_types.get()
def list_user_types(request):
	d = []
	for ut in session.query(UserType):
		d.append(ut.as_dict())
	return d

@user_update.post()
def update_user(request):
	log.debug('{}'.format(request.params))
	return {'hello': 'yes'}

@user_validate.post()
def validate_user(request):
	log.debug('{}'.format(request.params))
	return {'hello': 'yes'}

''' Recommender views '''

@recommender_collection.get()
def get_recommenders(request):
	# log.debug('{}'.format(request.params))
	# return {'hello': 'yes'}
	r = []
	for user in session.query(User).filter(User.user_type_id == 4):
		r.append({
			'id': int(user.id),
			'name': user.name,
			'email': user.email,
			'user_type': user.user_type.name,
			'date_created': str(user.date_created),
			'last_modified': str(user.last_modified)
		})
	return r

@recommender_create.post()
def create_recommender(request):
	log.debug('{}'.format(request.params))
	return {'hello': 'yes'}

@recommender_delete.post()
def delete_recommender(request):
	log.debug('{}'.format(request.params))
	return {'hello': 'yes'}

@recommender_show.get()
def show_recommender(request):
	log.debug('{}'.format(request.params))
	return {'hello': 'yes'}

@recommender_update.post()
def update_recommender(request):
	log.debug('{}'.format(request.params))
	return {'hello': 'yes'}

''' Form views '''

@form_collection.get()
def get_forms(request):
	log.debug('{}'.format(request.params))
	return {'hello': 'yes'}

@form_create.post()
def create_form(request):
	log.debug('{}'.format(request.params))
	return {'hello': 'yes'}

@form_delete.post()
def delete_form(request):
	log.debug('{}'.format(request.params))
	return {'hello': 'yes'}

@form_show.get()
def show_form(request):
	log.debug('{}'.format(request.params))
	return {'hello': 'yes'}

@form_update.post()
def update_form(request):
	log.debug('{}'.format(request.params))
	return {'hello': 'yes'}

''' Category views '''

@category_collection.get()
def get_categories(request):
	# log.debug('{}'.format(request.params))
	# return {'hello': 'yes'}
	c = []
	for item in session.query(Category).all():
		c.append({
			'id': int(item.id),
			'name': item.name,
			'date_created': str(item.date_created),
			'last_modified': str(item.last_modified),
			'form_type_id': item.form_type_id
	})
	return c

@category_create.post()
def create_category(request):
	log.debug('{}'.format(request.params))
	return {'hello': 'yes'}

@category_delete.post()
def delete_category(request):
	log.debug('{}'.format(request.params))
	return {'hello': 'yes'}

@category_show.get()
def show_category(request):
	log.debug('{}'.format(request.params))
	return {'hello': 'yes'}

@category_update.post()
def update_category(request):
	log.debug('{}'.format(request.params))
	return {'hello': 'yes'}

''' Question views '''

@question_collection.get()
def get_questions(request):
	# log.debug('{}'.format(request.params))
	# return {'hello': 'yes'}
	q = []
	for item in session.query(Question).all():
		q.append({
			'id': int(item.id),
			'name': item.name,
			'date_created': str(item.date_created),
			'last_modified': str(item.last_modified),
			'category_id': item.category_id
	})
	return q

@question_create.post()
def create_question(request):
	log.debug('{}'.format(request.params))
	return {'hello': 'yes'}

@question_delete.post()
def delete_question(request):
	log.debug('{}'.format(request.params))
	return {'hello': 'yes'}

@question_show.get()
def show_question(request):
	log.debug('{}'.format(request.params))
	return {'hello': 'yes'}

@question_update.post()
def update_question(request):
	log.debug('{}'.format(request.params))
	return {'hello': 'yes'}
