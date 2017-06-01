from webtest import TestApp
import unittest
from ngse import main
# from pyramid import testing
# from cornice import Service
import sys


login_testcases=[
	['ngse@coe.upd.edu.ph', 'ngse', True],
	['mfmayol@up.edu.ph', 'kz2xjiAm', True],
	['bmicons360@gmail.com', 'QFmy5jWg', True],
	['bmicons360@gmail.com', 'iaX6oHGy', True],
	['bmicons360@gmail.com', 'Yz8pcQPb', True],
	['bmicons360@gmail.com', 'sm6GlLLq', True],
	['sdnkskksdls', 'emknlnsklnkls', False],
	['msdksmkl', 'ngse@123', False],
	['ngse@coe.upd.edu.ph', 'msdkls', False],
]

view_user_testcases=[
	['2', True], #applicant
	['1', True], #admin
	['1000', False], #non existent user
	['', False] #null input
]

# update_application_status_testcases=[
# 	['2', 'notNull', True],
# 	# ['2', '', False],
# 	['1', 'notNull', False], #ADMIN
# 	['1', '', False],
# 	['3', 'notNull', False], #nnonexistent id
# 	['3', '', False],
# 	# ['', 'notNull', False],
# 	# ['', '', False]
# ]

view_answers_testcases=[
	['2', '5', True], #applicant
	['2', '100', False], #applicant invalid category
	['1000', '5', False], #non existent user
	['', '', False] #null input
]

# create_user_testcases=[
# 	['ngse@coe.upd.edu.ph', 'name', False],
# 	# ['valid@email.com', 'name', True],
# 	# ['', '', False],
# 	# ['', 'name', False]
# ]

show_form_testcases=[
	['1', True],
	['5', False]
]

class TestEndpoints(unittest.TestCase):
	app = TestApp(main({}))

	tokens = []

	def test_get_users(self):
		resp = self.app.get('/v1/users')
		print resp.json
		assert resp.status == '200 OK'

	def test_login(self):
		print '\n\n'
		for item in login_testcases:
			e = item[0]
			p = item[1]
			o = item[2]
			request = self.app.post('/v1/users/login', dict(email=e, password=p))
			if o:
				self.tokens.append(request.json['token'])
			print '{}, {}'.format(request.json['success'], o)
			self.assertEqual(request.json['success'], o)

	def test_tokens(self):
		print '\n\n'
		for token in self.tokens:
			request = self.app.post('/v1/users/verify', dict(token=token))
			print '{}'.format(request.json['message'])
			self.assertEqual(request.json['success'], True)


	def test_view_user(self):
		print '\n\n'
		for item in view_user_testcases:
			id = item[0]
			o = item[1]
			resp = self.app.get('/v1/users/show', dict(user_id=id))
			if not o:
				print resp.json
				self.assertEqual(resp.json['success'], o)
			else:
				assert resp.status == '200 OK'

	# def test_update_status(self):
	# 	print '\n\n'
	# 	for item in update_status_testcases:
	# 		id = item[0]
	# 		stat = item[1]
	# 		o = item[2]
	# 		# print id, stat, o
	# 		request = app.get('/v1/users/update_status', dict(user_id=id, user_status = stat))
	# 		self.assertEqual(request.json['success'], o)

	def test_view_answers(self):
		print '\n\n'
		for item in view_answers_testcases:
			id = item[0]
			cat_id = item[1]
			o = item[2]
			resp = self.app.get('/v1/users/answers/show', dict(user_id=id, category_id=cat_id))
			if o:
				assert resp.status == '200 OK'
			else:
				self.assertEqual(resp.json['success'], o)
		
	# def test_create_user(self):
	# 	print '\n\n'
	# 	for item in create_user_testcases:
	# 		e, n, o = item[0], item[1], item[2]
	# 		request = app.post('/v1/users/create', dict(email=e, name=n))
	# 		self.assertEqual(request.json['success'], o)

	def test_get_forms(self):
		print '\n\n'
		request = self.app.get('/v1/forms')
		self.assertEqual(request.status, '200 OK')

	def test_list_form_types(self):
		print '\n\n'
		request = self.app.get('/v1/forms/types')
		self.assertEqual(request.status, '200 OK')

	def test_show_form(self):
		print '\n\n'
		for  item in show_form_testcases:
			id = item[0]
			o = item[1]
			resp = self.app.get('/v1/forms/show', dict(form_id=id))
			print resp.json
			if o:
				assert resp.status == '200 OK'
			else:
				self.assertEqual(resp.json['success'], o)



if __name__ == '__main__':
	unittest.main()
   
