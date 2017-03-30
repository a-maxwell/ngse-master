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
import os

def setup(session):
	def add(obj):
		session.add(obj)
		session.commit()
		return obj

	dir_path = os.path.dirname(os.path.realpath(__file__))

	user_types = open('{}/initial/user_types.txt'.format(dir_path), 'r').read().splitlines()

	for user_type_name in user_types:
		# check user type
		try:
			user_type = session.query(UserType)\
			.filter(UserType.name == user_type_name)\
			.one()
		# make new entry if not found
		except NoResultFound as e:
			user_type = add(UserType(name=user_type_name))

	try:
		admin = session.query(User)\
		.filter(User.name == 'admin')\
		.one()
	except NoResultFound as e:
		admin = add(User(
			name="admin",
			email="ngse@coe.upd.edu.ph",
			password=bcrypt.hashpw('ngse', bcrypt.gensalt()),
			user_type_id=1
		))

	try:
		user = session.query(User)\
		.filter(User.name == 'user')\
		.one()
	except NoResultFound as e:
		user = add(User(
			name="user",
			email="user@upd.edu.ph",
			password=bcrypt.hashpw('ngse',bcrypt.gensalt()),
			user_type_id=3
		))

	form_types = open('{}/initial/form_types.txt'.format(dir_path), 'r').read().splitlines()

	application_form_sequence = [1,2,3,4,5,6,7,8,9]
	recommendation_letter_sequence = [10,11]

	for form_type_name in form_types:
		# check form type
		try:
			form_type = session.query(FormType)\
			.filter(FormType.name == form_type_name)\
			.one()
		# make new entry if not found
		except NoResultFound as e:
			form_type = add(FormType(
				name=form_type_name,
				page_sequence=application_form_sequence if\
				(form_type_name == "Application Form") else\
				(
					recommendation_letter_sequence if\
					(form_type_name == "Recommendation Letter") else []
				)
			))

		categories = open('{}/initial/{}/categories.txt'.format(dir_path, form_type_name), 'r').read().splitlines()

		for category_name in categories:
			# check category wrt form type
			try:
				category = session.query(Category)\
				.filter(Category.name == category_name)\
				.filter(Category.form_type_id == form_type.id)\
				.one()
			# make new entry if not found
			except NoResultFound as e:
				category = add(Category(name=category_name, form_type_id=form_type.id))

			questions = open('{}/initial/{}/{}/questions.txt'.format(dir_path, form_type_name, category_name), 'r').read().splitlines()

			for question_name in questions:
				fields = question_name.split(', ')

				name = fields[0]
				meta = {}
				if len(fields) > 1:
					choices = fields[1].split('; ')
					meta['choices'] = choices

				# check question wrt category
				try:
					q = session.query(Question)\
					.filter(Question.name == name)\
					.filter(Question.category_id == category.id)\
					.one()
					# check if meta is the same
				# make new entry if not found
				except NoResultFound as e:
					q = add(Question(name=name, category_id=category.id, meta=meta))

			answers = open('{}/initial/{}/{}/answers.txt'.format(dir_path, form_type_name, category_name), 'r').read().splitlines()

			for answer_name in answers:
				fields = answer_name.split(', ')
				name = fields[0]
				question_id = fields[1]
				user_id = fields[2]

				try:
					a = session.query(Answer)\
					.filter(Answer.name == answer_name)\
					.one()
				except NoResultFound as e:
					a = add(Answer(name=name, question_id=question_id, user_id=2))

	try:
		application_form = session.query(Form)\
			.filter(Form.name == 'Application Form')\
			.one()
	except NoResultFound as e:
		application_form = add(Form(
			name="Application Form",
			date_start="2017-03-01 01:00:00",
			date_end="2017-06-01 01:00:00",
			# page_sequence=application_form_sequence,
			form_type_id=1
		))

	try:
		recommendation_letter = session.query(Form)\
			.filter(Form.name == 'Recommendation Letter')\
			.one()
	except NoResultFound as e:
		recommendation_letter = add(Form(
			name="Recommendation Letter",
			date_start="2017-03-01 01:00:00",
			date_end="2017-06-01 01:00:00",
			# page_sequence=recommendation_letter_sequence,
			form_type_id=2
			))