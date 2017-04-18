import sqlalchemy
import os
from sqlalchemy.orm import sessionmaker
from setup import setup
from models import Base

def connect(user, password, db, host='localhost', port=5432):
	url = 'postgresql://{}:{}@{}:{}/{}'.format(user, password, host, port, db)

	if 'DATABASE_URL' in os.environ:
		url = os.environ['DATABASE_URL']


	db = sqlalchemy.create_engine(url, client_encoding='utf8')
	engine = db.connect()
	meta = sqlalchemy.MetaData(bind=engine, reflect=True)

	return db, engine, meta

''' Database setup '''

if 'TRAVIS' in  os.environ:
	db, engine, meta = connect('postgres', '', 'ngsewebsite')
else:
	db, engine, meta = connect('ngse', 'ngse', 'ngsewebsite')

# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
SessionFactory = sessionmaker(engine)
session = SessionFactory()
setup(session)
