from webtest import TestApp
import unittest
from ngse import main
# from pyramid import testing
# from cornice import Service
import sys



class ConditionTests(unittest.TestCase):
	def test_invalid_user_id(self):
		app = TestApp(main({}))
		data = 'yes'
		request = app.get('/v1/users/delete', dict(user_id=data, id=2, step=1))
		self.assertEqual(request.json['message'], 'user_id is invalid')
		
	def test_no_user_id(self):
		app = TestApp(main({}))
		request = app.get('/v1/users/delete', dict(id=2, step=1))	
		self.assertEqual(request.json['message'], 'user_id is missing')

	def test_valid_user_id(self):
		app = TestApp(main({}))
		data = 1
		request = app.get('/v1/users/delete', dict(user_id=data, id=2, step=1))	
		self.assertEqual(request.json['message'], 'user_id is valid')

	def test_invalid_id(self):
		app = TestApp(main({}))
		data = 'yes'
		request = app.get('/v1/users/delete', dict(user_id=1, id=data, step=2))
		self.assertEqual(request.json['message'], 'id is invalid')

	def test_no_id(self):
		app = TestApp(main({}))
		request = app.get('/v1/users/delete', dict(user_id=1, step=2))
		self.assertEqual(request.json['message'], 'id is missing')

	def test_valid_id(self):
		app = TestApp(main({}))
		data = 2
		request = app.get('/v1/users/delete', dict(user_id=1, id=data, step=2))
		self.assertEqual(request.json['message'], 'id is valid')

	def test_if_user_accessing_exists(self):
		app = TestApp(main({}))
		data = 1
		request = app.get('/v1/users/delete', dict(user_id=data, id=2, step=3))
		self.assertEqual(request.json['message'], 'user exists')

	def test_if_user_accessing_does_not_exist(self):
		app = TestApp(main({}))
		data = 100
		request = app.get('/v1/users/delete', dict(user_id=data, id=2, step=3))
		self.assertEqual(request.json['message'], 'user does not exist')

	def test_if_not_admin_but_same_id(self):
		app = TestApp(main({}))
		data = 2
		request = app.get('/v1/users/delete', dict(user_id=data, id=data, step=4))
		self.assertEqual(request.json['message'], 'user not admin but same id')

	def test_if_not_admin_but_diff_id(self):
		app = TestApp(main({}))
		data = 2
		request = app.get('/v1/users/delete', dict(user_id=data, id=1, step=4))
		self.assertEqual(request.json['message'], 'user not admin but diff id')
	
	def test_if_admin_but_diff_id(self):
		app = TestApp(main({}))
		data = 1
		request = app.get('/v1/users/delete', dict(user_id=data, id=2, step=4))
		self.assertEqual(request.json['message'], 'admin trying to delete other account')
	
	def test_if_admin_but_same_id(self):
		app = TestApp(main({}))
		data = 1
		request = app.get('/v1/users/delete', dict(user_id=data, id=data, step=4))
		self.assertEqual(request.json['message'], 'admin trying to delete admin account')

	def test_other_user_does_not_exist(self):
		app = TestApp(main({}))
		data = 100
		request = app.get('/v1/users/delete', dict(user_id=1, id=data, step=5))
		self.assertEqual(request.json['message'], 'other user does not exist')

	def test_other_user_exists(self):
		app = TestApp(main({}))
		data = 2
		request = app.get('/v1/users/delete', dict(user_id=1, id=data, step=5))
		self.assertEqual(request.json['message'], 'other user exists')

if __name__ == '__main__':
	unittest.main()
   
