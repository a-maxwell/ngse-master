from webtest import TestApp
import unittest
from ngse import main
from pyramid import testing
from cornice import Service
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

class test_ngse(unittest.TestCase):
	def test_login(self):
		app=TestApp(main({}))
		for item in login_testcases:
			e = item[0]
			p = item[1]
			o = item[2]
			request = app.get('/v1/login', dict(email=e, password=p))
			print request.json['success']
			self.assertEqual(request.json['success'], o)
	def test_get_users(self):
		app = TestApp(main({}))
		resp = app.get('/v1/users')
		assert resp.status == '200 OK'
		

if __name__ == '__main__':
	unittest.main()
   