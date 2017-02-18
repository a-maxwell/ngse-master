from cornice import Service
import logging

log = logging.getLogger(__name__)

URI = {
	# resources
	'users': '/users',
	'recommenders': '/recommenders',
	'forms': '/forms',
	'categories': '/categories',
	'questions': '/questions',
	# actions
	'authorize': '/authorize',
	'create': '/create',
	'delete': '/delete',
	'search': '/search',
	'show': '/show',
	'update': '/update',
	'validate': '/validate'
}

def encapsulate(primary, secondary='', action='', base='/v1'):
	return base+primary+secondary+action

def create_resource(resource, primary, secondary=''):
	return {
		'collection': Service(name=resource, path=encapsulate(primary, secondary), renderer='json', description="Fetch list of {}".format(resource)),
		'actions': {
			'create': Service(name='create {}'.format(resource), path=encapsulate(primary, secondary, URI['create']), renderer='json', description="Create {}".format(resource)),
			'delete': Service(name='delete {}'.format(resource), path=encapsulate(primary, secondary, URI['delete']), renderer='json', description="Delete {}".format(resource)),
			'show': Service(name='show {}'.format(resource), path=encapsulate(primary, secondary, URI['show']), renderer='json', description="Show {} information".format(resource)),
			'update': Service(name='update {}'.format(resource), path=encapsulate(primary, secondary, URI['update']), renderer='json', description="Update {} information".format(resource))
		}
	}

user = create_resource("user", URI['users'])
user['actions']['authorize'] = Service(name='authorize user', path=encapsulate(URI['users'], URI['authorize']), description="Return JWT upon successful authorization")
user['actions']['search'] = Service(name='search user', path=encapsulate(URI['users'], URI['search']), description="Search for set of users")
user['actions']['validate'] = Service(name='validate user', path=encapsulate(URI['users'], URI['validate']), description="Validate the status of the user")

user_collection = user['collection']
user_authorize = user['actions']['authorize']
user_create = user['actions']['create']
user_delete = user['actions']['delete']
user_search = user['actions']['search']
user_show = user['actions']['show']
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

''' User views '''

@user_collection.get()
def get_users(request):
	log.debug('{}'.format(request.params))
	return {'hello': 'yes'}

@user_authorize.post()
def authorize_user(request):
	log.debug('email: {}, password: {}'.format(request.params['email'], request.params['password']))
	return {'hello': 'yes'}

@user_create.post()
def create_user(request):
	log.debug('{}'.format(request.params))
	return {'hello': 'yes'}

@user_delete.post()
def delete_user(request):
	log.debug('{}'.format(request.params))
	return {'hello': 'yes'}

@user_search.get()
def search_user(request):
	log.debug('{}'.format(request.params))
	return {'hello': 'yes'}

@user_show.get()
def show_user(request):
	log.debug('{}'.format(request.params))
	return {'hello': 'yes'}

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
	log.debug('{}'.format(request.params))
	return {'hello': 'yes'}

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
	log.debug('{}'.format(request.params))
	return {'hello': 'yes'}

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
	log.debug('{}'.format(request.params))
	return {'hello': 'yes'}

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
