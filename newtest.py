from webtest import TestApp
import unittest
from ngse import main
# from pyramid import testing
# from cornice import Service
import sys

login_TestCases=[
	['ngse@coe.upd.edu.ph', 'ngse', True],
	['wrongEmail@coe.upd.edu.ph', 'ngse', False],
	['ngse@coe.upd.edu.ph', 'wrongPassword', False],
	['wrongEmail@coe.upd.edu.ph', 'wrongPassword', False]
]

createUser_TestCases = [
	['new1@email.com', 'Lastname', 'Firstname', 'MidName', '3', True],
	['new2@email.com', 'Lastname', 'Firstname', 'MidName', '4', True],
	['new3@email.com', 'Lastname', 'Firstname', 'MidName', '5', True],
	['new1@email.com', 'Lastname', 'Firstname', 'MidName', '5', False],
	['new2@email.com', 'Lastname', 'Firstname', 'MidName', '3', False],
	['new3@email.com', 'Lastname', 'Firstname', 'MidName', '4', False],
]

deleteUser_TestCases = [
	['14', '2', False],
	['15', '3', False],
	['16', '4', False],
	# ['14', '1', True],
	# ['15', '1', True],
	# ['16', '1', True],
]


updateAstatus_TestCases = [
	['2','Accepted', True],
	['8','Accepted', False],
]

updateVstatus_TestCases=[
	['2', 'Complete', True],
	['8', 'Complete', False]
]

updateAnswer_TestCases = [
	['2', 'newname', 1, True]
]


class Test_Functional(unittest.TestCase):
	app = TestApp(main({}))

	def test_Login(self):
		print '\n\n'
		for item in login_TestCases:
			e = item[0]
			p = item[1]
			o = item[2]
			request = self.app.post('/v1/users/login', dict(email=e, password=p))
			# print request.json['success']
			self.assertEqual(request.json['success'], o)

	# def test_CreateUser(self):
	# 	print '\n\n'
	# 	for item in createUser_TestCases:
	# 		request = self.app.post('/v1/users/create', dict(email=item[0], last=item[1], given=item[2], middlemaiden=item[3], level=item[4]))
	# 		self.assertEqual(request.json['success'], item[5])

	def test_DeleteUser(self):
		print '\n\n'
		for item in deleteUser_TestCases:
			request = self.app.get('/v1/users/delete', dict(user_id=item[0], id=item[1]))
			self.assertEqual(request.json['success'], item[2])

	def test_UpdateAstatus(self):
		print '\n\n'
		for item in updateAstatus_TestCases:
			request = self.app.get('/v1/users/update_a_status', dict(user_id=item[0], a_status=item[1]))
			self.assertEqual(request.json['success'], item[2])

	def test_UpdateVstatus(self):
		print '\n\n'
		for item in updateVstatus_TestCases:
			request = self.app.get('/v1/users/update_v_status', dict(user_id=item[0], v_status=item[1]))
			self.assertEqual(request.json['success'], item[2])

	def test_UpdateAnswer(self):
		print '\n\n'
		for item in updateAnswer_TestCases:
			request = self.app.post('/v1/users/answers/update', dict(user_id=item[0], data=item[1], length=item[2]))
			self.assertEqual(request.json['success'], item[3])
'''
class Test_UpdateApplicationStatus(unittest.TestCase):
	def test_dataFlow1(self):
		print '\n\n'
		request = self.app.get('/v1/users/update_a_status', dict(user_id=2, a_status='Accepted'))
		self.assertEqual(request.json['id'], '2')

	def test_dataFlow2(self):
		print '\n\n'
		request = self.app.get('/v1/users/update_a_status', dict(user_id=2, a_status='Accepted'))
		self.assertEqual(request.json['status'], 'Accepted')

	def test_dataFlow3(self):
		print '\n\n'
		request = self.app.get('/v1/users/update_a_status', dict(user_id=2, a_status='Accepted'))
		self.assertEqual(request.json['old_status'], 'None')

	def test_ConditionTest_Pass1(self):
		print '\n\n'
		request = self.app.get('/v1/users/update_a_status', dict(user_id=1, a_status='Accepted'))
		self.assertEqual(request.json['success'], False)

	def test_ConditionTest_Pass2(self):
		print '\n\n'
		request = self.app.get('/v1/users/update_a_status', dict(user_id=4, a_status='Accepted'))
		self.assertEqual(request.json['success'], False)

	def test_ConditionTest_Fail(self):
		print '\n\n'
		request = self.app.get('/v1/users/update_a_status', dict(user_id=2, a_status='Accepted'))
		self.assertEqual(request.json['success'], True)

	def test_dataFlow4(self):
		print '\n\n'
		request = self.app.get('/v1/users/update_a_status', dict(user_id=2, a_status='Accepted'))
		self.assertEqual(request.json['new_status'], 'Accepted')

	def test_dataFlow5(self):
		print '\n\n'
		request = self.app.get('/v1/users/update_a_status', dict(user_id=2, a_status='Accepted'))
		self.assertEqual(request.json['success'], True)

class Test_UpdateValidationStatus(unittest.TestCase):
	def test_dataFlow1(self):
		print '\n\n'
		request = self.app.get('/v1/users/update_v_status', dict(user_id=2, v_status='Submitted'))
		self.assertEqual(request.json['id'], '2')

	def test_dataFlow2(self):
		print '\n\n'
		request = self.app.get('/v1/users/update_v_status', dict(user_id=2, v_status='Submitted'))
		self.assertEqual(request.json['status'], 'Submitted')

	def test_dataFlow3(self):
		print '\n\n'
		request = self.app.get('/v1/users/update_v_status', dict(user_id=2, v_status='Submitted'))
		self.assertEqual(request.json['old_status'], 'None')

	def test_ConditionTest_Pass1(self):
		print '\n\n'
		request = self.app.get('/v1/users/update_v_status', dict(user_id=1, v_status='Submitted'))
		self.assertEqual(request.json['success'], False)

	def test_ConditionTest_Pass2(self):
		print '\n\n'
		request = self.app.get('/v1/users/update_v_status', dict(user_id=4, v_status='Submitted'))
		self.assertEqual(request.json['success'], False)

	def test_ConditionTest_Fail(self):
		print '\n\n'
		request = self.app.get('/v1/users/update_v_status', dict(user_id=2, v_status='Submitted'))
		self.assertEqual(request.json['success'], True)

	def test_dataFlow4(self):
		print '\n\n'
		request = self.app.get('/v1/users/update_v_status', dict(user_id=2, v_status='Submitted'))
		self.assertEqual(request.json['new_status'], 'Submitted')

	def test_dataFlow5(self):
		print '\n\n'
		request = self.app.get('/v1/users/update_v_status', dict(user_id=2, v_status='Submitted'))
		self.assertEqual(request.json['success'], True)
'''
# class ConditionTests(unittest.TestCase):
# 	def test_invalid_user_id(self):
# 		print '\n\n'
# 		data = 'yes'
# 		request = self.app.get('/v1/users/delete', dict(user_id=data, id=2, step=1))
# 		self.assertEqual(request.json['message'], 'user_id is invalid')
		
# 	def test_no_user_id(self):
# 		print '\n\n'
# 		request = self.app.get('/v1/users/delete', dict(id=2, step=1))	
# 		self.assertEqual(request.json['message'], 'user_id is missing')

# 	def test_valid_user_id(self):
# 		print '\n\n'
# 		data = 1
# 		request = self.app.get('/v1/users/delete', dict(user_id=data, id=2, step=1))	
# 		self.assertEqual(request.json['message'], 'user_id is valid')

# 	def test_invalid_id(self):
# 		print '\n\n'
# 		data = 'yes'
# 		request = self.app.get('/v1/users/delete', dict(user_id=1, id=data, step=2))
# 		self.assertEqual(request.json['message'], 'id is invalid')

# 	def test_no_id(self):
# 		print '\n\n'
# 		request = self.app.get('/v1/users/delete', dict(user_id=1, step=2))
# 		self.assertEqual(request.json['message'], 'id is missing')

# 	def test_valid_id(self):
# 		print '\n\n'
# 		data = 2
# 		request = self.app.get('/v1/users/delete', dict(user_id=1, id=data, step=2))
# 		self.assertEqual(request.json['message'], 'id is valid')

# 	def test_if_user_accessing_exists(self):
# 		print '\n\n'
# 		data = 1
# 		request = self.app.get('/v1/users/delete', dict(user_id=data, id=2, step=3))
# 		self.assertEqual(request.json['message'], 'user exists')

# 	def test_if_user_accessing_does_not_exist(self):
# 		print '\n\n'
# 		data = 100
# 		request = self.app.get('/v1/users/delete', dict(user_id=data, id=2, step=3))
# 		self.assertEqual(request.json['message'], 'user does not exist')

# 	def test_if_not_admin_but_same_id(self):
# 		print '\n\n'
# 		data = 2
# 		request = self.app.get('/v1/users/delete', dict(user_id=data, id=data, step=4))
# 		self.assertEqual(request.json['message'], 'user not admin but same id')

# 	def test_if_not_admin_but_diff_id(self):
# 		print '\n\n'
# 		data = 2
# 		request = self.app.get('/v1/users/delete', dict(user_id=data, id=1, step=4))
# 		self.assertEqual(request.json['message'], 'user not admin but diff id')
	
# 	def test_if_admin_but_diff_id(self):
# 		print '\n\n'
# 		data = 1
# 		request = self.app.get('/v1/users/delete', dict(user_id=data, id=2, step=4))
# 		self.assertEqual(request.json['message'], 'admin trying to delete other account')
	
# 	def test_if_admin_but_same_id(self):
# 		print '\n\n'
# 		data = 1
# 		request = self.app.get('/v1/users/delete', dict(user_id=data, id=data, step=4))
# 		self.assertEqual(request.json['message'], 'admin trying to delete admin account')

# 	def test_other_user_does_not_exist(self):
# 		print '\n\n'
# 		data = 100
# 		request = self.app.get('/v1/users/delete', dict(user_id=1, id=data, step=5))
# 		self.assertEqual(request.json['message'], 'other user does not exist')

# 	def test_other_user_exists(self):
# 		print '\n\n'
# 		data = 2
# 		request = self.app.get('/v1/users/delete', dict(user_id=1, id=data, step=5))
# 		self.assertEqual(request.json['message'], 'other user exists')

# 	def test_bva_min_1(self):
# 		print '\n\n'
# 		data = 0
# 		request = self.app.get('/v1/users/delete', dict(user_id=1, id=data, step=2))
# 		self.assertEqual(request.json['message'], 'id must not be less than 1')

# 	def test_bva_between(self):
# 		print '\n\n'
# 		data = 2
# 		request = self.app.get('/v1/users/delete', dict(user_id=1, id=data, step=2))
# 		self.assertEqual(request.json['message'], 'id is valid')

# 	def test_bva_max_1(self):
# 		print '\n\n'
# 		data = 2147483648
# 		request = self.app.get('/v1/users/delete', dict(user_id=1, id=data, step=2))
# 		self.assertEqual(request.json['message'], 'id is too large')

# class Test(unittest.TestCase):
	# def test_1(self): #test that val is what's expected
	# 	print '\n\n'
	# 	resp = self.app.get('/v1/users/answers', dict(user_id='2'))
	# 	# print resp
	# 	self.assertEqual(resp.json['id'], '2')
	# def test_2(self): #test that db querry's output is correct
	# 	print '\n\n'
	# 	resp = self.app.get('/v1/users/answers', dict(user_id='3'))
		# self.assertEqual(resp.json['u_name'], 'user')
	# def test_3(self): #test that errors are handled 
	# 	print '\n\n'
	# 	resp = self.app.get('/v1/users/answers', dict(user_id=''))
	# 	self.assertEqual(resp.json['success'], False)
	# def test_4a(self): #test conditions(or): non existing val making cond true
	# 	print '\n\n'
	# 	resp = self.app.get('/v1/users/answers', dict(user_id='3')) 
	# 	self.assertEqual(resp.json['success'], False)
	# def test_4b(self): #test conditions(or): existing val making cond false
	# 	print '\n\n'
	# 	resp = self.app.get('/v1/users/answers', dict(user_id='2'))
	# 	self.assertEqual(resp.json['success'], True)
	# def test_5a(self): #test conditions(or): user is admin making cond true
	# 	print '\n\n'
	# 	resp = self.app.get('/v1/users/answers', dict(user_id='1'))
	# 	self.assertEqual(resp.json['success'], False)
	# def test_5b(self): #test conditions (or): user is applicant making cond false
	# 	print '\n\n'
	# 	resp = self.app.get('/v1/users/answers', dict(user_id='2'))
	# 	self.assertEqual(resp.json['success'], True)
	# def test_6(self): #data flow test that data is what's expected
	# 	print '\n\n'
	# 	resp = self.app.get('/v1/users/answers', dict(user_id='2'))
	# 	self.assertEqual(resp.json['list'], [])
	# def test_7a(self): #loop test: boundary val(start)
	# 	print '\n\n'
	# 	resp = self.app.get('/v1/users/answers', dict(user_id='2'))
	# 	self.assertEqual(resp.json['categ'], 'Basic Information')
	# def test_7b(self): #loop test: boundary val (end)
	# 	print '\n\n'
	# 	resp = self.app.get('/v1/users/answers', dict(user_id='2'))
	# 	print resp
	# 	self.assertEqual(resp.json['categ'], 'References')
	# def test_8(self): #data flow
	# 	print '\n\n'
	# 	resp = self.app.get('/v1/users/answers', dict(user_id='2'))
	# 	print resp
	# 	self.assertEqual(resp.json['list'], [])
	# def test_9a(self): #loop test: inner loop boundary val(start)
	# 	print '\n\n'
	# 	resp = self.app.get('/v1/users/answers', dict(user_id='2'))
	# 	self.assertEqual(resp.json['q'], 'Last Name')
	# def test_9b(self): #loop test: inner loop boundary val(end)
	# 	print '\n\n'
	# 	resp = self.app.get('/v1/users/answers', dict(user_id='2'))
	# 	self.assertEqual(resp.json['q'], 'E-mail Address')
	# def test_10a(self): #data flow/loop test: checks if data is correct sa boundary val (start)
	# 	print '\n\n'
	# 	resp = self.app.get('/v1/users/answers', dict(user_id='2'))
	# 	self.assertEqual(resp.json['name'], 'user surname')
	# def test_10b(self):#data flow/loop test: checks if data is correct sa boundary val (end)
	# 	print '\n\n'
	# 	resp = self.app.get('/v1/users/answers', dict(user_id='2'))
	# 	self.assertEqual(resp.json['name'], 'sdafrvsdvwfdffsbgeadr')
	# def test_11a(self): # condition test: make the cond false; q_id=1 (ans to q1 exists)
	# 	print '\n\n'
	# 	resp = self.app.get('/v1/users/answers', dict(user_id='2'))
	# 	self.assertEqual(resp.json['success'], True)
	# def test_11b(self): #condition test: make the condition true; q_id=4 (non-existing answer)
	# 	print '\n\n'
	# 	resp = self.app.get('/v1/users/answers', dict(user_id='2'))
	# 	self.assertEqual(resp.json['success'], False)
	# def test_12(self): #data flow
	# 	print '\n\n'
	# 	resp = self.app.get('/v1/users/answers', dict(user_id='2'))
	# 	self.assertEqual(resp.json['ans'], 'user surname')
	# def test_13a(self): # only first question and answer is in the array; len = 1
	# 	print '\n\n'
	# 	resp = self.app.get('/v1/users/answers', dict(user_id='2'))
	# 	self.assertEqual(resp.json['q_array'], [{'question': 'Last Name' , 'answer': 'user surname' }])
	# def test_13b(self): # all data expected should be in the array; len = n, categ = 1
	# 	print '\n\n'
	# 	resp = self.app.get('/v1/users/answers', dict(user_id='2'))
	# 	
	# 	self.assertEqual(resp.json['q_array'], [{'question': 'Last Name' , 'answer': 'user surname' },
	# 											{'question': 'Given Name' , 'answer': 'user given name' },
	# 											{'question': 'Middle/Maiden Name' , 'answer': 'user middle name' },
	# 											])
	# def test_13c(self): # first data when categ = 2; len = 1
	# 	print '\n\n'
	# 	resp = self.app.get('/v1/users/answers', dict(user_id='2'))
	# 	print resp
	# 	self.assertEqual(resp.json['q_array'], [{'question': 'Level of Degree' , 'answer': None }])
	# def test_14a(self): # all data expected should be in the array when categ = 1; len = n, categ = 1
	# 	print '\n\n'
	# 	resp = self.app.get('/v1/users/answers', dict(user_id='2'))
	# 	
	# 	self.assertEqual(resp.json['categ'], [{'name':'Basic Information', 'data': [{'question': 'Last Name' , 'answer': 'user surname' },
	# 																				{'question': 'Given Name' , 'answer': 'user given name' },
	# 																				{'question': 'Middle/Maiden Name' , 'answer': 'user middle name' },
	# 																				]
	# 											}])
	# def test_14b(self): # all data expected should be in the array when categ = 2(mid categ for apps, boundary val) 
	# 	print '\n\n'
	# 	resp = self.app.get('/v1/users/answers', dict(user_id='2'))
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
	# 	print '\n\n'
	# 	resp = self.app.get('/v1/users/answers', dict(user_id='2'))
	# 	self.assertEqual(len(resp.json['data']), 9)

if __name__ == '__main__':
	unittest.main()
   
