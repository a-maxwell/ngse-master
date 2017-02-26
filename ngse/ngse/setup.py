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
import os

def setup(session):
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
			user_type = UserType(name=user_type_name)
			session.add(user_type)
			session.commit()

	admin = User(name="admin", email="ngse@coe.upd.edu.ph", password="ngse", user_type_id=1)
	session.add(admin)
	session.commit()

	form_types = open('{}/initial/form_types.txt'.format(dir_path), 'r').read().splitlines()

	for form_type_name in form_types:
		# check form type
		try:
			form_type = session.query(FormType)\
			.filter(FormType.name == form_type_name)\
			.one()

		# make new entry if not found
		except NoResultFound as e:
			form_type = FormType(name=form_type_name)
			session.add(form_type)
			session.commit()

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
				category = Category(name=category_name, form_type_id=form_type.id)
				session.add(category)
				session.commit()

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
					question = session.query(Question)\
					.filter(Question.name == name)\
					.filter(Question.category_id == category.id)\
					.one()
					# check if meta is the same
				# make new entry if not found
				except NoResultFound as e:
					question = Question(name=name, category_id=category.id, meta=meta)
					session.add(question)
					session.commit()