import logging
log = logging.getLogger(__name__)

JWT_SECRET = "NationalGraduateSchoolOfEng'g"

URI = {
	# resources
	'users': '/users',
	'recommenders': '/recommenders',
	'forms': '/forms',
	'categories': '/categories',
	'questions': '/questions',
	# actions
	'verify': '/verify',
	'login': '/login',
	'create': '/create',
	'delete': '/delete',
	'search': '/search',
	'show': '/show',
	'types': '/types',
	'update': '/update',
	'validate': '/validate'
}

def encapsulate(primary, secondary='', action='', base='/v1'):
	return base+primary+secondary+action
