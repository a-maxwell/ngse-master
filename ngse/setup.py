from sqlalchemy.orm.exc import NoResultFound
import bcrypt
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
		}
	]
	if not os.environ.get('GMAILUSERNAME') is None:
		users = [
			{
				'name': 'NGSE Staff',
				'email': os.environ['GMAILUSERNAME'],
				'password': os.environ['GMAILPASSWORD'],
				'user_type_id': 1
			}
		]
	answers = {
	}
	forms = [
		{
			'name': 'Non-ERDT Application Form',
			'date_start': '2017-03-01 01:00:00',
			'date_end': '2017-07-01 01:00:00',
			'form_type_id': 2
		},
		{
			'name': 'ERDT Application Form',
			'date_start': '2017-03-01 01:00:00',
			'date_end': '2017-07-01 01:00:00',
			'form_type_id': 3
		},
		{
			'name': 'Recommendation Letter',
			'date_start': '2017-03-01 01:00:00',
			'date_end': '2017-07-01 01:00:00',
			'form_type_id': 1
		}
	]

	def add(obj):
		session.add(obj)
		session.commit()
		return obj

	def setup_categories():
		categories = open('{}/initial/categories.txt'.format(dir_path), 'r').read().splitlines()
		for category_name in categories:
			# print 'checked {}'.format(category_name)
			# check category 
			try:
				category = session.query(Category)\
				.filter(Category.name == category_name)\
				.one()
			# make new entry if not found
			except NoResultFound as e:
				category = add(Category(name=category_name))

			'''please do this pio huhuhuhu'''
			elements = json.loads(open('{}/initial/categories/{}.json'.format(dir_path, category_name), 'r').read())
			# continue

			for element in elements:
				# print 'checked q \'{}\''.format(question['title'])
				# check element wrt category
				try:
					q = session.query(Element)\
					.filter(Element.name == element['name'])\
					.filter(Element.category_id == category.id)\
					.one()
					# check if meta is the same
				# make new entry if not found
				except NoResultFound as e:
					q = Element(name=element['name'], category_id=category.id, klass=element['klass'], kind=element['kind'], text=element['text'])
					q.width = element.get('width', 16)
					q.required = element.get('required', None)
					q.choices = element.get('choices', None)
					q.default = element.get('default', None)
					add(q)

	def setup_forms(forms):
		form_types = open('{}/initial/form_types.txt'.format(dir_path), 'r').read().splitlines()
		for form_type_name in form_types:
			# print 'checked {}'.format(form_type_name)
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

				for category_id in form['category_ids']:
					print '{} and {}'.format(form_type.id, category_id)
					
					try:
						session.query(form_category_association)\
						.filter(form_category_association.c.form_types_id == form_type.id)\
						.filter(form_category_association.c.categories_id == category_id)\
						.one()
					except:
						add(form_category_association(
							form_type_id = form_type.id,
							categories_id = category_id
						))

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
			# print 'checked {}'.format(user_type_name)
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

		for k, v in answers.iteritems():
			user = session.query(User)\
				.filter(User.user_type_id == k)\
				.one()

			for element_id, text in v.iteritems():
				try:
					session.query(Answer)\
					.filter(Answer.user_id == user.id)\
					.filter(Answer.element_id == element_id)\
					.one()
				except:
					add(Answer(
						name = text,
						element_id = element_id,
						user_id = user.id
					))
	def setup_applicant_attrs(users):
			for u in users:
				if u['user_type_id'] in [4,5]:
					_u = session.query(User)\
					.filter(User.name == u['name'])\
					.one()
					try:
						session.query(ApplicantAttribute)\
						.filter(ApplicantAttribute.applicant_id == _u.id)\
						.one()
					except NoResultFound as e:
						if u['user_type_id'] == 4:	
							add(ApplicantAttribute(
								recommender_a = 3,
								recommender_b = 4,
								applicant_id = _u.id
							))

						else:
							add(ApplicantAttribute(
								scholarship = True,
								recommender_a = 5,
								applicant_id = _u.id
							))
	setup_categories()
	setup_users(users)
	setup_forms(forms)
	# setup_applicant_attrs(users)
