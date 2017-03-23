from webtest import TestApp
import unittest
from ngse import main

import sys

class Test(unittest.TestCase):
	# def test_1(self): #test that val is what's expected
	# 	app=TestApp(main({}))
	# 	resp = app.get('/v1/users/answers', dict(user_id='2'))
	# 	# print resp
	# 	self.assertEqual(resp.json['id'], '2')
	# def test_2(self): #test that db querry's output is correct
	# 	app=TestApp(main({}))
	# 	resp = app.get('/v1/users/answers', dict(user_id='3'))
		# self.assertEqual(resp.json['u_name'], 'user')
	# def test_3(self): #test that errors are handled 
	# 	app=TestApp(main({}))
	# 	resp = app.get('/v1/users/answers', dict(user_id=''))
	# 	self.assertEqual(resp.json['success'], False)
	# def test_4a(self): #test conditions(or): non existing val making cond true
	# 	app=TestApp(main({}))
	# 	resp = app.get('/v1/users/answers', dict(user_id='3')) 
	# 	self.assertEqual(resp.json['success'], False)
	# def test_4b(self): #test conditions(or): existing val making cond false
	# 	app=TestApp(main({}))
	# 	resp = app.get('/v1/users/answers', dict(user_id='2'))
	# 	self.assertEqual(resp.json['success'], True)
	# def test_5a(self): #test conditions(or): user is admin making cond true
	# 	app=TestApp(main({}))
	# 	resp = app.get('/v1/users/answers', dict(user_id='1'))
	# 	self.assertEqual(resp.json['success'], False)
	# def test_5b(self): #test conditions (or): user is applicant making cond false
	# 	app=TestApp(main({}))
	# 	resp = app.get('/v1/users/answers', dict(user_id='2'))
	# 	self.assertEqual(resp.json['success'], True)
	# def test_6(self): #data flow test that data is what's expected
	# 	app=TestApp(main({}))
	# 	resp = app.get('/v1/users/answers', dict(user_id='2'))
	# 	self.assertEqual(resp.json['list'], [])
	# def test_7a(self): #loop test: boundary val(start)
	# 	app=TestApp(main({}))
	# 	resp = app.get('/v1/users/answers', dict(user_id='2'))
	# 	self.assertEqual(resp.json['categ'], 'Basic Information')
	# def test_7b(self): #loop test: boundary val (end)
	# 	app=TestApp(main({}))
	# 	resp = app.get('/v1/users/answers', dict(user_id='2'))
	# 	print resp
	# 	self.assertEqual(resp.json['categ'], 'References')
	# def test_8(self): #data flow
	# 	app=TestApp(main({}))
	# 	resp = app.get('/v1/users/answers', dict(user_id='2'))
	# 	print resp
	# 	self.assertEqual(resp.json['list'], [])
	# def test_9a(self): #loop test: inner loop boundary val(start)
	# 	app=TestApp(main({}))
	# 	resp = app.get('/v1/users/answers', dict(user_id='2'))
	# 	self.assertEqual(resp.json['q'], 'Last Name')
	# def test_9b(self): #loop test: inner loop boundary val(end)
	# 	app=TestApp(main({}))
	# 	resp = app.get('/v1/users/answers', dict(user_id='2'))
	# 	self.assertEqual(resp.json['q'], 'E-mail Addresss')
	# def test_10a(self): #data flow/loop test: checks if data is correct sa boundary val (start)
	# 	app=TestApp(main({}))
	# 	resp = app.get('/v1/users/answers', dict(user_id='2'))
	# 	self.assertEqual(resp.json['name'], 'user surname')
	# def test_10b(self):#data flow/loop test: checks if data is correct sa boundary val (end)
	# 	app=TestApp(main({}))
	# 	resp = app.get('/v1/users/answers', dict(user_id='2'))
	# 	self.assertEqual(resp.json['name'], 'sdafrvsdvwfdffsbgeadr')
	# def test_11a(self): # condition test: make the cond false; q_id=1 (ans to q1 exists)
	# 	app=TestApp(main({}))
	# 	resp = app.get('/v1/users/answers', dict(user_id='2'))
	# 	self.assertEqual(resp.json['success'], True)
	# def test_11b(self): #condition test: make the condition true; q_id=4 (non-existing answer)
	# 	app=TestApp(main({}))
	# 	resp = app.get('/v1/users/answers', dict(user_id='2'))
	# 	self.assertEqual(resp.json['success'], False)
	# def test_12(self): #data flow
	# 	app=TestApp(main({}))
	# 	resp = app.get('/v1/users/answers', dict(user_id='2'))
	# 	self.assertEqual(resp.json['ans'], 'user surname')
	# def test_13a(self): # only first question and answer is in the array; len = 1
	# 	app=TestApp(main({}))
	# 	resp = app.get('/v1/users/answers', dict(user_id='2'))
	# 	self.assertEqual(resp.json['q_array'], [{'question': 'Last Name' , 'answer': 'user surname' }])
	# def test_13b(self): # all data expected should be in the array; len = n, categ = 1
	# 	app=TestApp(main({}))
	# 	resp = app.get('/v1/users/answers', dict(user_id='2'))
	# 	
	# 	self.assertEqual(resp.json['q_array'], [{'question': 'Last Name' , 'answer': 'user surname' },
	# 											{'question': 'Given Name' , 'answer': 'user given name' },
	# 											{'question': 'Middle/Maiden Name' , 'answer': 'user middle name' },
	# 											])
	# def test_13c(self): # first data when categ = 2; len = 1
	# 	app=TestApp(main({}))
	# 	resp = app.get('/v1/users/answers', dict(user_id='2'))
	# 	print resp
	# 	self.assertEqual(resp.json['q_array'], [{'question': 'Level of Degree' , 'answer': None }])
	# def test_14a(self): # all data expected should be in the array when categ = 1; len = n, categ = 1
	# 	app=TestApp(main({}))
	# 	resp = app.get('/v1/users/answers', dict(user_id='2'))
	# 	
	# 	self.assertEqual(resp.json['categ'], [{'name':'Basic Information', 'data': [{'question': 'Last Name' , 'answer': 'user surname' },
	# 																				{'question': 'Given Name' , 'answer': 'user given name' },
	# 																				{'question': 'Middle/Maiden Name' , 'answer': 'user middle name' },
	# 																				]
	# 											}])
	# def test_14b(self): # all data expected should be in the array when categ = 2(mid categ for apps, boundary val) 
	# 	app=TestApp(main({}))
	# 	resp = app.get('/v1/users/answers', dict(user_id='2'))
	# 	# print resp
	# 	self.assertEqual(resp.json['categ'], 	[{'name':'Basic Information', 'data': [{'question': 'Last Name' , 'answer': 'user surname' },
	# 																				{'question': 'Given Name' , 'answer': 'user given name' },
	# 																				{'question': 'Middle/Maiden Name' , 'answer': 'user middle name' },
	# 																				]
	# 											},
	# 											{'name':'Program of Study', 'data': [
	# 													{'question': 'Level of Degree' , 'answer': None },
	# 													{'question': 'Degree Program' , 'answer': None },
	# 													{'question': 'Thesis Option' , 'answer': None },
	# 													{'question': 'Full-Time or Part-Time' , 'answer': None },
	# 													{'question': 'Choices of Research Field' , 'answer': None },
	# 													{'question': 'Intended start of Program Study' , 'answer': None },
	# 													{'question': 'Academic Year' , 'answer': None },
	# 													{'question': 'Applying for anotother scholarship/grant' , 'answer': None },
	# 													{'question': 'Name of scholarship program you are applying for' , 'answer': None },
	# 													{'question': 'Name of potential research adviser' , 'answer': None }
	# 													]
	# 											}])
	# def test_15(self): #test that na-output nya lahat
	# 	app=TestApp(main({}))
	# 	resp = app.get('/v1/users/answers', dict(user_id='2'))
	# 	self.assertEqual(len(resp.json['data']), 9)

	
if __name__ == '__main__':
	unittest.main()
   
