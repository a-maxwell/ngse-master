from webtest import TestApp
import unittest
from ngse import main

import sys

class Test(unittest.TestCase):
	# def test_1(self):
	# 	app=TestApp(main({}))
	# 	resp = app.get('/v1/users/answers', dict(user_id='2'))
	# 	# print resp
	# 	self.assertEqual(resp.json['id'], '2')
	# def test_2(self):
	# 	app=TestApp(main({}))
	# 	resp = app.get('/v1/users/answers', dict(user_id='3'))
		# self.assertEqual(resp.json['u_name'], 'user')
	# def test_3(self):
	# 	app=TestApp(main({}))
	# 	resp = app.get('/v1/users/answers', dict(user_id=''))
	# 	self.assertEqual(resp.json['success'], False)
	# def test_4(self):
	# 	app=TestApp(main({}))
	# 	resp = app.get('/v1/users/answers', dict(user_id='3'))
	# 	self.assertEqual(resp.json['success'], True)
	# def test_4_2(self):
	# 	app=TestApp(main({}))
	# 	resp = app.get('/v1/users/answers', dict(user_id='2'))
	# 	self.assertEqual(resp.json['success'], False)
	# def test_5_1(self):
	# 	app=TestApp(main({}))
	# 	resp = app.get('/v1/users/answers', dict(user_id='1'))
	# 	self.assertEqual(resp.json['success'], True)
	# def test_5_2(self):
	# 	app=TestApp(main({}))
	# 	resp = app.get('/v1/users/answers', dict(user_id='2'))
	# 	self.assertEqual(resp.json['success'], False)
	# def test_6(self):
	# 	app=TestApp(main({}))
	# 	resp = app.get('/v1/users/answers', dict(user_id='2'))
	# 	self.assertEqual(resp.json['list'], [])
	# def test_7a(self):
	# 	app=TestApp(main({}))
	# 	resp = app.get('/v1/users/answers', dict(user_id='2'))
	# 	self.assertEqual(resp.json['categ'], 'Basic Information')
	# def test_7b(self):
	# 	app=TestApp(main({}))
	# 	resp = app.get('/v1/users/answers', dict(user_id='2'))
	# 	print resp
	# 	self.assertEqual(resp.json['categ'], 'References')
	# def test_8(self):
	# 	app=TestApp(main({}))
	# 	resp = app.get('/v1/users/answers', dict(user_id='2'))
	# 	print resp
	# 	self.assertEqual(resp.json['list'], [])
	# def test_9a(self):
	# 	app=TestApp(main({}))
	# 	resp = app.get('/v1/users/answers', dict(user_id='2'))
	# 	self.assertEqual(resp.json['q'], 'Last Name')
	# def test_9b(self):
	# 	app=TestApp(main({}))
	# 	resp = app.get('/v1/users/answers', dict(user_id='2'))
	# 	self.assertEqual(resp.json['q'], 'E-mail Addresss')
	# def test_10a(self):
	# 	app=TestApp(main({}))
	# 	resp = app.get('/v1/users/answers', dict(user_id='2'))
	# 	self.assertEqual(resp.json['name'], 'user surname')
	def test_10b(self):
		app=TestApp(main({}))
		resp = app.get('/v1/users/answers', dict(user_id='2'))
		self.assertEqual(resp.json['name'], 'sdafrvsdvwfdffsbgeadr')


if __name__ == '__main__':
	unittest.main()
   
