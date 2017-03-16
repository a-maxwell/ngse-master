from cornice import Service
import json
import sqlalchemy

# from pyramid.httpexceptions import HTTPFound
# from pyramid.security import remember, forget
# from pyramid.security import authenticated_userid
# from pyramid.security import unauthenticated_userid
# from pyramid.security import (
#     Authenticated,
#     Everyone,
# 	Allow
# )
import bcrypt
import jwt
import os
import time
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
from utils import encapsulate, URI, log
from setup import setup
from database import session
import endpoint


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

form = create_resource("form", URI['forms'],
	extra=[
		{
			'key': 'types',
			'name': 'list form types',
			'description': 'List all types of forms'
		}
	])

form_collection = form['collection']
form_create = form['actions']['create']
form_delete = form['actions']['delete']
form_show = form['actions']['show']
form_types = form['actions']['types']
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


''' User views '''
login_url = '/v1/login'
view_answers_url = '/v1/users/answers'
update_answer_url = 'v1/users/update_answer'
view_status_url = 'v1/users/status'
update_status_url = 'v1/users/update_status'
user_login = Service(name='user_login', path=login_url, description="logging in")
view_answers = Service(name='view_answers', path=view_answers_url, description="view answers")
view_status = Service(name='view_status', path=view_status_url, description="view user's application status")
update_answer = Service(name='update_answer', path=update_answer_url, description="update answer")
update_status = Service(name='update_status', path=update_status_url, description="update user's application status")


def is_authenticated(request):
	#returns null if not logged in
	#else returns id of loged in user
	return authenticated_userid(request)

# @user_login.get()
endpoint.login = user_login.get()(endpoint.login)
endpoint.answer_update = update_answer.get()(endpoint.answer_update)
endpoint.view_answer = view_answers.get()(endpoint.view_answer)
endpoint.get_users = user_collection.get()(endpoint.get_users)
endpoint.authorize_user = user_authorize.post()(endpoint.authorize_user)
endpoint.create_user = user_create.post()(endpoint.create_user)
endpoint.view_user_status = view_status.get()(endpoint.view_user_status)
endpoint.update_user_status = update_status.get()(endpoint.update_user_status)

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

	department = request.params["department"]

	users = session.query(User).join(Answer)\
		.filter(Answer.name == department)\
		.all()

	d = []
	for user in users:
		d.append({
			'id': int(user.id),
			'name': user.name,
			'email': user.email,
			'application_status': user.application_status
		})

	return d

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
	id = request.params['id']

	user = session.query(User)\
		.filter(User.id == id)\
		.one()


	answers = session.query(Answer)\
		.filter(Answer.user_id == id)\
		.all()

	a = []

	for answer in answers:
		a.append({
			'question_id': answer.question_id,
			'question': answer.question.name,
			'answer_id': answer.id,
			'name': answer.name
			})

	return {
		'name': user.name,
		'date_created': str(user.date_created),
		'last_modified': str(user.last_modified),
		'email': user.email,
		'application_status': user.application_status,
		'user_type': user.user_type.name,
		'answers': a
	}

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

endpoint.get_forms = form_collection.get()(endpoint.get_forms)
endpoint.create_form = form_create.get()(endpoint.create_form)
endpoint.delete_form = form_delete.get()(endpoint.delete_form)
endpoint.show_form = form_show.get()(endpoint.show_form)
endpoint.update_form = form_update.get()(endpoint.update_form)
endpoint.list_form_types = form_types.get()(endpoint.list_form_types)

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
