from webtest import TestApp
import unittest
from ngse import main
# from pyramid import testing
# from cornice import Service
import sys


login_testcases=[
	['ngse@coe.upd.edu.ph', 'ngse', True],
	['', 'ngse', False],
	['ngse@coe.upd.edu.ph', '', False],
	['', '', False],
	['wrongEmail@coe.upd.edu.ph', 'ngse', False],
	['ngse@coe.upd.edu.ph', 'wrongPassword', False],
	['wrongEmail@coe.upd.edu.ph', 'wrongPassword', False],
		

]
view_status_testcases=[
	# ['2', True], #applicant
	['1', False], #admin
	['3', False], #non existent user
	['', False] #null input
]

update_status_testcases=[
	['2', 'notNull', True],
	# ['2', '', False],
	['1', 'notNull', False], #ADMIN
	['1', '', False],
	['3', 'notNull', False], #nnonexistent id
	['3', '', False],
	# ['', 'notNull', False],
	# ['', '', False]
]

view_answers_testcases=[
	['2', True], #applicant
	['1', False], #admin
	['3', False], #non existent user
	['', False] #null input
]

create_user_testcases=[
	['ngse@coe.upd.edu.ph', 'name', False],
	# ['valid@email.com', 'name', True],
	# ['', '', False],
	# ['', 'name', False]
]

show_form_testcases=[
	['1', True],
	['3', False]
]

class test_ngse(unittest.TestCase):
	def test_login(self):
		app=TestApp(main({}))
		for item in login_testcases:
			e = item[0]
			p = item[1]
			o = item[2]
			request = app.get('/v1/login', dict(email=e, password=p))
			# print request.json['success']
			self.assertEqual(request.json['success'], o)

	def test_get_users(self):
		app = TestApp(main({}))
		resp = app.get('/v1/users')
		assert resp.status == '200 OK'

	def test_view_status(self):
		app = TestApp(main({}))
		for item in view_status_testcases:
			id = item[0]
			o = item[1]
			request = app.get('/v1/users/status', dict(user_id=id))
			# print request.json['success']
			self.assertEqual(request.json['success'], o)

	def test_update_status(self):
		app = TestApp(main({}))
		for item in update_status_testcases:
			id = item[0]
			stat = item[1]
			o = item[2]
			# print id, stat, o
			request = app.get('/v1/users/update_status', dict(user_id=id, user_status = stat))
			self.assertEqual(request.json['success'], o)

	def test_view_answers(self):
		app = TestApp(main({}))
		for item in view_answers_testcases:
			id = item[0]
			o = item[1]
			request = app.get('/v1/users/answers', dict(user_id=id))
			print request.json['success']
			self.assertEqual(request.json['success'], o)
		
	def test_create_user(self):
		app = TestApp(main({}))
		for item in create_user_testcases:
			e, n, o = item[0], item[1], item[2]
			request = app.post('/v1/users/create', dict(email=e, name=n))
			self.assertEqual(request.json['success'], o)

	def test_get_forms(self):
		app = TestApp(main({}))
		request = app.get('/v1/forms')
		self.assertEqual(request.status, '200 OK')

	def test_list_form_types(self):
		app = TestApp(main({}))
		request = app.get('/v1/forms/types')
		self.assertEqual(request.status, '200 OK')

	def test_show_form(self):
		app = TestApp(main({}))
		for  item in show_form_testcases:
			id = item[0]
			request = app.get('/v1/forms/show', dict(id=id))
			self.assertEqual(request.status, '200 OK')
if __name__ == '__main__':
	unittest.main()
   
