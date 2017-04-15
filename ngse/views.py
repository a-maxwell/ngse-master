from cornice import Service
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
	form_category_association
)
from utils import encapsulate, decode, encode, generateError, generateSuccess, URI, log

from database import session
from validators import *
from endpoint import *

from pyramid.view import view_config

@view_config(route_name='index', renderer='index.html')
def index(request):
	sections = [
		{'name': 'home', 'icon': 'home'},
		{'name': 'news', 'icon': 'announcement'},
		{'name': 'about', 'icon': 'book'},
		{'name': 'documents', 'icon': 'file text outline'},
		{'name': 'contact', 'icon': 'mail'},
		{'name': 'auth', 'icon': 'sign in'},
	]
	return {'sections': sections}

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

###############################################################################

user = create_resource("user", URI['users'], extra=[{'key': 'verify', 'name': 'verify user', 'description': 'Verify user token'},{'key': 'login', 'name': 'login user', 'description': 'Return JWT upon successful login'}])

users_get = user['collection']
get_users = (users_get).get()(get_users)

user_verify = user['actions']['verify']
verify_user = user_verify.post()(verify_user)

user_login = user['actions']['login']
login_user = user_login.post()(login_user)

user_create = user['actions']['create']
create_user = user_create.post()(create_user)

user_delete = user['actions']['delete']
delete_user = user_delete.get()(delete_user)

user_show = user['actions']['show']
show_user = user_show.get()(show_user)

user_update = user['actions']['update']
@user_update.post()
def update_user(request):
	log.debug('{}'.format(request.params))
	return {'hello': 'yes'}

###############################################################################

recommender = create_resource("recommender", URI['users'], URI['recommenders'])

recommender_collection = recommender['collection']
recommender_create = recommender['actions']['create']
recommender_delete = recommender['actions']['delete']
recommender_show = recommender['actions']['show']
recommender_update = recommender['actions']['update']

###############################################################################

form = create_resource("form", URI['forms'], extra=[{'key': 'types','name': 'list form types','description': 'List all types of forms'}])

forms_get = form['collection']
# get_forms = forms_get.get(validators=(has_token))(get_forms)
get_forms = forms_get.get(validators=())(get_forms)

form_create = form['actions']['create']
create_form = form_create.get(validators=(has_token, has_admin_rights))(create_form)

form_delete = form['actions']['delete']
delete_form = form_delete.get(validators=(has_token, has_admin_rights))(delete_form)

form_show = form['actions']['show']
# show_form = form_show.get(validators=(has_token, has_form_id))(show_form)
show_form = form_show.get()(show_form)

form_update = form['actions']['update']
update_form = form_update.get()(update_form)

form_types_get = form['actions']['types']
get_form_types = form_types_get.get()(get_form_types)

###############################################################################

category = create_resource("category", URI['forms'], URI['categories'])

categories_get = category['collection']
get_categories = categories_get.get(validators=())(get_categories)

category_create = category['actions']['create']

category_delete = category['actions']['delete']

category_show = category['actions']['show']
show_category = category_show.get()(show_category)

category_update = category['actions']['update']


###############################################################################

question = create_resource("question", URI['forms']+URI['categories'], URI['questions'])

questions_get = question['collection']
get_questions = questions_get.get()(get_questions)

question_create = question['actions']['create']
question_delete = question['actions']['delete']
question_show = question['actions']['show']
question_update = question['actions']['update']

###############################################################################

answer = create_resource("answer", URI['users'], URI['answers'])

answers_get = answer['collection']
get_answers = answers_get.get()(get_answers)

answer_create = answer['actions']['create']

answer_delete = answer['actions']['delete']

answer_show = answer['actions']['show']

answer_update = answer['actions']['update']
update_answer = answer_update.get()(update_answer)

###############################################################################

view_answers_url = '/v1/users/answers'
update_answer_url = 'v1/users/update_answer'
view_status_url = 'v1/users/status'
update_status_url = 'v1/users/update_status'
# user_login = Service(name='user_login', path=login_url, description="logging in")
view_answers = Service(name='view_answers', path=view_answers_url, description="view answers")
# view_status = Service(name='view_status', path=view_status_url, description="view user's application status")
update_answer = Service(name='update_answer', path=update_answer_url, description="update answer")
# update_status = Service(name='update_status', path=update_status_url, description="update user's application status")

###############################################################################

# answer_update = update_answer.get()(answer_update)
view_answer = view_answers.get()(view_answer)

''' User views '''

# @user_search.get()
# def search_user(request):

# 	department = request.params["department"]

# 	users = session.query(User).join(Answer)\
# 		.filter(Answer.name == department)\
# 		.all()

# 	d = []
# 	for user in users:
# 		d.append({
# 			'id': int(user.id),
# 			'name': user.name,
# 			'email': user.email,
# 			'application_status': user.application_status
# 		})

# 	return d

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

''' Category views '''


@category_create.post()
def create_category(request):
	log.debug('{}'.format(request.params))
	return {'hello': 'yes'}

@category_delete.post()
def delete_category(request):
	log.debug('{}'.format(request.params))
	return {'hello': 'yes'}

@category_update.post()
def update_category(request):
	log.debug('{}'.format(request.params))
	return {'hello': 'yes'}

''' Question views '''

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
