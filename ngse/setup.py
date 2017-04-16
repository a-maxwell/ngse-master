from sqlalchemy.orm.exc import NoResultFound
import bcrypt
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
import json
import os

def setup(session):
	dir_path = os.path.dirname(os.path.realpath(__file__))
	users = [
		{
			'name': 'admin',
			'email': 'ngse@coe.upd.edu.ph',
			'password': 'ngse',
			'user_type_id': 1
		},
		{
			'name': 'user',
			'email': 'user@upd.edu.ph',
			'password': 'ngse',
			'user_type_id': 4
		},
		{
			'name': 'erdt',
			'email': 'erdt@upd.edu.ph',
			'password': 'ngse',
			'user_type_id': 3
		},
		{
			'name': 'rec',
			'email': 'rec@upd.edu.ph',
			'password': 'ngse',
			'user_type_id': 5
		}
	]
	forms = [
		{
			'name': 'Non-ERDT Application Form',
			'date_start': '2017-03-01 01:00:00',
			'date_end': '2017-06-01 01:00:00',
			'form_type_id': 1
		},
		{
			'name': 'ERDT Application Form',
			'date_start': '2017-03-01 01:00:00',
			'date_end': '2017-06-01 01:00:00',
			'form_type_id': 2
		},
		{
			'name': 'Recommendation Letter',
			'date_start': '2017-03-01 01:00:00',
			'date_end': '2017-06-01 01:00:00',
			'form_type_id': 3
		}
	]

	def add(obj):
		session.add(obj)
		session.commit()
		return obj

	def setup_categories():
		categories = open('{}/initial/categories.txt'.format(dir_path), 'r').read().splitlines()
		for category_name in categories:
			print 'checked {}'.format(category_name)
			# check category 
			try:
				category = session.query(Category)\
				.filter(Category.name == category_name)\
				.one()
			# make new entry if not found
			except NoResultFound as e:
				category = add(Category(name=category_name))

			'''please do this pio huhuhuhu'''
			questions = json.loads(open('{}/initial/categories/{}.json'.format(dir_path, category_name), 'r').read())
			# continue

			for question in questions:
				print 'checked q \'{}\''.format(question['title'])
				# check question wrt category
				try:
					q = session.query(Question)\
					.filter(Question.name == question['title'])\
					.filter(Question.category_id == category.id)\
					.one()
					# check if meta is the same
				# make new entry if not found
				except NoResultFound as e:
					q = Question(name=question['title'], category_id=category.id, input_type=question['class'])
					q.choices = question.get('choices', None)
					add(q)

	def setup_forms(forms):
		form_types = open('{}/initial/form_types.txt'.format(dir_path), 'r').read().splitlines()
		for form_type_name in form_types:
			print 'checked {}'.format(form_type_name)
			# check form type
			try:
				form_type = session.query(FormType)\
				.filter(FormType.name == form_type_name)\
				.one()
			# make new entry if not found
			except NoResultFound as e:
				data = open('{}/initial/forms/{}.json'.format(dir_path, form_type_name)).read()
				form = json.loads(data)

				categories = []
				for category_id in form['category_ids']:
					categories.append(session.query(Category)\
						.filter(Category.id == category_id)\
						.one()
					)

				form_type = FormType(
					name = form['name'],
					page_sequence = form['category_ids'],
					user_type_id = form['user_id']
				)
				form_type.categories = categories
				add(form_type)

		for f in forms:
			try:
				session.query(Form)\
					.filter(Form.name == f['name'])\
					.one()
			except NoResultFound as e:
				add(Form(
					name = f['name'],
					date_start = f['date_start'] ,
					date_end = f['date_end'],
					form_type_id = f['form_type_id']
				))

	def setup_users(users):
		user_types = open('{}/initial/user_types.txt'.format(dir_path), 'r').read().splitlines()
		for user_type_name in user_types:
			print 'checked {}'.format(user_type_name)
			# check user type
			try:
				user_type = session.query(UserType)\
				.filter(UserType.name == user_type_name)\
				.one()
			# make new entry if not found
			except NoResultFound as e:
				user_type = add(UserType(name=user_type_name))

		for u in users:
			try:
				session.query(User)\
				.filter(User.name == u['name'])\
				.one()
			except NoResultFound as e:
				add(User(
					name = u['name'],
					email = u['email'],
					password = bcrypt.hashpw(u['password'], bcrypt.gensalt()),
					user_type_id = u['user_type_id']
				))

	setup_categories()
	setup_users(users)
	setup_forms(forms)