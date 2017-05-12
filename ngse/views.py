from cornice import Service
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
# changes in daisy

print_form_url = 'v1/print'
print_form = Service(name='print_form', path=print_form_url, description="print form")
forms = print_form.get()(forms)
# view_answers_url = '/v1/users/answers' #new : users/answers/show
update_answer_url = 'v1/users/update_answer'
update_application_status_url = 'v1/users/update_a_status'

# view_status_url = 'v1/users/status'
update_validation_status_url = 'v1/users/update_v_status'
reset_database_url = 'v1/delete_all'
# view_answers = Service(name='view_answers', path=view_answers_url, description="view answers")
# update_answer = Service(name='update_answer', path=update_answer_url, description="update answer")
# update_a_status = Service(name='update_a_status', path=update_application_status_url, description="update user's application status")

# view_status = Service(name='view_v_status', path=view_status_url, description="view user's form validation status and application status")
# update_v_status = Service(name='update_v_status', path=update_validation_status_url, description="update user's form validation status")
reset_db = Service(name='reset_db', path=reset_database_url, description="truncate tables in database")

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
update_user = user_update.post()(update_user)



# update_validation_status = update_v_status.get()(update_validation_status)
reset_database = reset_db.get()(reset_database)

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

# question = create_resource("question", URI['forms']+URI['categories'], URI['questions'])

# questions_get = question['collection']
# get_questions = questions_get.get()(get_questions)

# question_create = question['actions']['create']
# question_delete = question['actions']['delete']
# question_show = question['actions']['show']
# question_update = question['actions']['update']

element = create_resource("element", URI['forms']+URI['categories'], URI['elements'])

elements_get = element['collection']
get_elements = elements_get.get()(get_elements)

element_create = element['actions']['create']
element_delete = element['actions']['delete']
element_show = element['actions']['show']
element_update = element['actions']['update']

###############################################################################

answer = create_resource("answer", URI['users'], URI['answers'])

answers_get = answer['collection']
get_answers = answers_get.get()(get_answers)

answer_create = answer['actions']['create']

answer_delete = answer['actions']['delete']

answer_show = answer['actions']['show']
show_answer = answer_show.get()(show_answer)

answer_update = answer['actions']['update']
update_answer = answer_update.post()(update_answer)

###############################################################################

# answer_update = update_answer.get()(answer_update)
# view_answer = view_answers.get()(view_answer)

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

''' Element views '''

@element_create.post()
def create_element(request):
	log.debug('{}'.format(request.params))
	return {'hello': 'yes'}

@element_delete.post()
def delete_element(request):
	log.debug('{}'.format(request.params))
	return {'hello': 'yes'}

@element_show.get()
def show_element(request):
	log.debug('{}'.format(request.params))
	return {'hello': 'yes'}

@element_update.post()
def update_element(request):
	log.debug('{}'.format(request.params))
	return {'hello': 'yes'}
