import logging
import sqlalchemy
log = logging.getLogger(__name__)

def connect(user, password, db, host='localhost', port=5432):
	url = 'postgresql://{}:{}@{}:{}/{}'.format(user, password, host, port, db)

	db = sqlalchemy.create_engine(url, client_encoding='utf8')
	engine = db.connect()
	meta = sqlalchemy.MetaData(bind=engine, reflect=True)

	return db, engine, meta

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
	'types': '/types',
	'update': '/update',
	'validate': '/validate'
}

def encapsulate(primary, secondary='', action='', base='/v1'):
	return base+primary+secondary+action
