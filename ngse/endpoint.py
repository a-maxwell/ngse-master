from database import session
from sqlalchemy.orm.exc import (NoResultFound, MultipleResultsFound)
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
	ApplicantAttribute,
	CategoryStatus
)

from utils import encode, decode, log, generateError, generateSuccess, generateToken, is_past, word, password_generator
from utils import send_credentials_email, send_recommender_email
from pyramid.response import FileResponse, Response
import bcrypt

from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Rect
from reportlab.lib.colors import black, gray

#################Page 1######################
def NGSE01(c, ans):
	c.showPage()
	c.setFont('Helvetica-Bold', 8)
	c.setFillColor(gray)
	c.drawString(58, 800, "Form NGSE-01")

def header(c, ans):
	c.setFont('Helvetica-Bold', 8)
	c.setFillColor(gray)
	c.drawString(58, 800, "Form NGSE-01")
	c.setFont('Helvetica-Bold', 16)
	c.setFillColor(black)
	c.drawCentredString(306,760, 'National Graduate School of Engineering')
	c.setFont('Helvetica', 12)
	c.drawCentredString(306,748,'College of Engineering')
	c.drawCentredString(306,736,'UNIVERSITY OF THE PHILIPPINES')
	c.drawCentredString(306,725,'Diliman, Quezon City 1101 Philippines')

	c.setFont('Helvetica-Bold', 20)
	c.drawCentredString(306,680,'APPLICATION FORM')
	c.setFont('Helvetica-Bold', 12)
	c.drawCentredString(306,670,'Admission to the Graduate Program')
	photobox(c, ans)

def photobox(c, ans):
	c.setStrokeColor(gray)
	c.rect(475, 705, 90, 90, stroke=1, fill=0)
	c.setFont('Times-Italic', 10)
	c.setFillColor(gray)
	c.drawCentredString(520, 760, "Staple two pieces")
	c.drawCentredString(520, 750, "of passport-sized")
	c.drawCentredString(520, 740, "photographs here")
	name(c, ans)

def name(c, ans):
	c.setStrokeColor(black)
	c.setFont('Helvetica', 14)
	c.setFillColor(black)
	c.rect(40, 635, 526, 25, stroke=1, fill=0)
	################NAME#########################
	c.drawCentredString(140, 642, ans['lastname'])
	c.drawCentredString(306, 642, ans['givenname'])
	c.drawCentredString(472, 642, ans['middlename'])
	#################NAME#########################
	c.setFont('Times-Italic', 10)
	c.setFillColor(black)
	c.drawCentredString(140, 625, "Last Name")
	c.drawCentredString(306, 625, "Given Name")
	c.drawCentredString(472, 625, "Middle/Maiden Name")
	instruct(c, ans)

def instruct(c, ans):
	c.setStrokeColor(black)
	c.rect(40, 580, 526, 20, stroke=1, fill=0)
	c.setFont('Helvetica-Bold', 15)
	c.setFillColor(black)
	c.drawCentredString(306, 584, "INSTRUCTIONS")
	c.rect(40, 353, 526, 247, stroke=1, fill=0)
	c.setFont('Helvetica', 9)
	array = []
	curr = 568
	for i in xrange(20):
		array.append(curr)
		curr = curr-13
	c.drawString(45, array[0], "1. Accomplish properly Form NGSE-01.")
	c.drawString(45, array[1], "2. Pay a nonrefundable application fee of PHP100.00 for Filipino and resident foreign applicants at the Cashier's Office. For ")
	c.drawString(45, array[2], "non-resident applicants, send a check of USD 20.00 payable to the 'University of the Philippines' together with the application")
	c.drawString(45, array[3], "documents.")
	c.drawString(45, array[4], "3. Request three (3) former professors or technical experts acting as your supervisor as references to accomplish Form NGSE-02.")
	c.drawString(45, array[5], "Each accomplished form should be enclosed in a sealed envelope, with a signature across the seal. Accomplished forms may be")
	c.drawString(45, array[6], "returned to the applicant or may be sent directly to the NGSE Office.")
	c.drawString(45, array[7], "4. Submit all the accomplished forms together with the following requirements:")
	c.drawString(45, array[8], "	- One (1) official copy and two (2) photocopies of Transcript of Records bearing the school seal and the registrar's signature")
	c.drawString(45, array[9], "   - Application fee receipt")
	c.drawString(45, array[10], "   - Three (3) recent passport size pictures")
	c.drawString(45, array[11], "   - Original and one (1) photocopy of NSO Birth Certificate (for Filipino applicants)")
	c.drawString(45, array[12], "   - Photocopy of passport (for foreign applicants)")
	c.drawString(45, array[13], "   - TOEFL official score (Only for foreign applicants whose native language or primary medium of instruction in secondary school")
	c.drawString(45, array[14], "   and college is not English). A score of at least 61 in the internetbased Test of English as a Foreign Language (Educational")
	c.drawString(45, array[15], "   Testing Service, Princeton, New Jersey, 08540 USA) is required.")
	c.drawString(45, array[16], "5. Wait for the final decision on your application, which will be communicated to you by email and/or phone.")
	NGSE(c, ans)

def NGSE(c, ans):
	c.setFont('Helvetica-Bold', 13)
	c.drawCentredString(305, 310, "For National Graduate School of Engineering Office Use Only")
	c.setFont('Helvetica', 9)
	c.setFillColor(gray)
	c.drawCentredString(305, 300, "(To the Applicant: Do not fill this portion)")
	c.setFont('Helvetica', 11)
	c.setFillColor(black)
	c.drawString(50, 278, "Date of Submission:")
	c.line(150, 278, 250, 278)
	c.drawString(310, 278, "O.R. Number:")
	c.line(380, 278, 500, 278)
	c.drawString(84, 268, "Received by:")
	c.line(150, 268, 250, 268)
	c.rect(310, 230, 200, 40, stroke=1)
	Dept(c, ans)

def Dept(c, ans):
	c.setFont('Helvetica-Bold', 13)
	c.drawCentredString(305, 210, "For Department/Institute/Program Admission Committee Use Only")
	c.setFont('Helvetica', 9)
	c.setFillColor(gray)
	c.drawCentredString(305, 200, "(To the Applicant: Do not fill this portion)")
	c.setFont('Helvetica', 11)
	c.setFillColor(black)
	c.drawString(50, 180, "The Department/Institute/Program Admission Committee recommends that the applicant be")
	c.rect(58, 160, 10, 10, stroke=1)
	c.drawString(75, 162, "admitted as a graduate degree student")
	c.rect(58, 144, 10, 10, stroke=1)
	c.drawString(75, 146, "admitted as a non-degree student (probationary admission) subject to the following condition(s):")
	c.line(80, 134, 540, 134)
	c.line(80, 124, 540, 124)
	c.line(80, 114, 540, 114)
	c.rect(58, 100, 10, 10, stroke=1)
	c.drawString(75, 102,"refused admission")
	c.line(70, 70, 350, 70)
	c.setFont('Helvetica-Bold', 9)
	c.drawCentredString(210, 60,"Department Chairman/Institute Director/Program Coordinator")
	c.drawCentredString(210, 50,"Printed Name")
	c.line(440, 70, 500, 70)
	c.drawCentredString(470, 60,"Date")

#############Page 2####################

def ProgramOfStudy(c, ans):
	NGSE01(c, ans)
	c.setFont('Helvetica-Bold', 14)
	c.setFillColor(black)
	c.drawString(40, 760, "I.   PROGRAM OF STUDY")
	c.setFont('Helvetica', 10)
	#########Degree Program##########
	c.drawString(50, 740, "1.a.	 Degree Program: Master of Science in Computer Science")
	#########Thesis Option###########
	c.drawString(50, 725, "1.b.	 THESIS OPTION")
	#########Full-Time###############
	c.drawString(50, 710, "1.c.	 Full-Time")
	ThesisOption(c, ans) ###IF THESIS OPTION###
	######Start of Study#####
	c.drawString(50, 635, "1.e.	 Intended start of program study: First Semester AY 2020-2021")
	######Scholarship#######
	c.drawString(50, 620, "1.f.	  Applying for another scholarship/grant? Yes")
	c.drawString(100, 605, "		 Name of Scholarship Program: ERDT")
	c.drawString(50, 590, "1.g.	 For THESIS OPTION:")
	c.drawString(100, 575, "		 Name of Potential Adviser:")

def ThesisOption(c, ans):
	c.drawString(50, 695, "1.d.	 For THESIS OPTION:")
	c.drawString(100, 680, "RANK 1:	CSG")
	c.drawString(100, 665, "RANK 2:	NDSG")
	c.drawString(100, 650, "RANK 3:	CVMIG")


def PersonalInfo(c, ans):
	c.setFont('Helvetica-Bold', 14)
	c.setFillColor(black)
	c.drawString(40, 550, "II.  PERSONAL INFORMATION")
	c.setFont('Helvetica', 10)
	c.drawString(50, 530, "2.a.")
	c.drawString(100, 530, "Last Name: " + ans['lastname'])
	c.drawString(100, 515, "Given Name: " + ans['givenname'])
	c.drawString(100, 500, "Middle Name: " + ans['middlename'])
	c.drawString(100, 470, "Country of Origin: " + ans['countryoforigin'])
	c.drawString(100, 485, "Citizenship: " + ans['citizenship'])
	c.drawString(350, 530, "Gender: " + ans['sex'])
	c.drawString(350, 515, "Birth Date: " + ans['birthdate'])
	c.drawString(350, 500, "Birth Place: " + ans['birthplace'])
	c.drawString(350, 485, "Civil Status: " + ans['civilstatus'])

	c.drawString(50, 440, "2.b.")
	c.drawString(100, 440, "Current Address: " + ans['currentaddress'])
	c.drawString(100, 425, "Postal Code: " + ans['currentpostal'])
	c.drawString(100, 410, "Permanent Address:" + ans['permanentaddress'])
	c.drawString(100, 395, "Postal Code: " + ans['permanentpostal'])

	c.drawString(50, 365, "2.c.")
	c.drawString(100, 365, "Telephone Number: " + ans['telephonenumber'])
	c.drawString(100, 350, "Fax Number: " + ans['faxnumber'])
	c.drawString(100, 335, "Email Address: " + ans['emailaddress'])

	c.drawString(50, 315, "2.d.")
	c.drawString(100, 315, "Father's Name: " + ans['fathersname'])
	c.drawString(100, 300, "Mpther's Name: " + ans['mothersname'])

	c.drawString(50, 270, "2.e.")
	c.drawString(100, 270, "Emergency Contact Person: " + ans['emergencyname'])
	# c.drawString(100, 290, "Complete Name: ")
	c.drawString(100, 255, "Complete Address: " + ans['emergencyaddress'])
	c.drawString(100, 240, "Relationship: " + ans['emergencyrelationship'])
	c.drawString(100, 220, "Contact Number: " + ans['emergencynumber'])


def EmploymentInfo(c, ans):
	c.setFont('Helvetica-Bold', 14)
	c.setFillColor(black)
	c.drawString(40, 195, "III.  EMPLOYMENT INFORMATION")
	c.setFont('Helvetica', 10)
	c.drawString(50, 175, "3.a.")
	c.drawString(100, 175, "Current Employment Status: " + ans['curremploymentstatus'])

	c.drawString(50, 155, "3.b.")
	c.drawString(100, 155, "Current Employed Applicants(Full-Time/Part-Time)")
	c.drawString(100, 140, "Position:" + ans['curremployedposition'])
	c.drawString(100, 125, "Company Name: " + ans['curremployedcompanyname'])
	c.drawString(100, 110, "Office Address: " + ans['curremployedofficeaddr'])
	c.drawString(100, 95, "E-mail Address: " + ans['curremployedcompanyemail'])
	c.drawString(350, 140, "Length of Service: " + ans['curremployedlengthofservice'])
	c.drawString(350, 125, "Telephone Number: " + ans['curremployedcompanytelenum'])
	c.drawString(350, 110, "Fax Number: " + ans['curremployedfaxnum'])
	c.drawString(350, 95, "Company Website: " + ans['curremployedcompanywebsite'])

	c.drawString(50, 75, "3.c.")
	c.drawString(100, 75, "Self-Employed Applicants")
	c.drawString(100, 60, "Business Name: " + ans['selfemployedbusinessname'])
	c.drawString(100, 45, "Business Address:" + ans['selfemployedbusinessaddress'])
	c.drawString(100, 30, "E-mail/Website: "  + ans['selfemployedbusinessemail'])
	c.drawString(350, 60, "Type of Business: "  + ans['selfemployedbusinesstype'] )
	c.drawString(350, 45, "Telephone Number: "  + ans['selfemployedbusinesstelnum'])
	c.drawString(350, 30, "Years of Operation: "  + ans['selfemployedyearsofoper'])

	################Page 3###############

	NGSE01(c, ans)
	c.setFillColor(black)
	c.setFont('Helvetica', 10)
	c.drawString(50, 760, "3.d.")
	c.drawString(100, 760, "Employment History")
	c.rect(65, 650, 500, 100, stroke=1)


def AcadBg(c, ans):
	c.setFont('Helvetica-Bold', 14)
	c.setFillColor(black)
	c.drawString(40, 630, "IV. ACADEMIC BACKGROUND")
	c.setFont('Helvetica', 10)
	c.drawString(50, 610, "4.a")
	c.drawString(100, 610, "Secondary Education")
	c.drawString(100, 595, "Last High School Attended")
	c.drawString(100, 580, "School Name: "  + ans['secondaryeducschoolname'])
	c.drawString(100, 565, "School Address: "  + ans['secondaryeducschooladdress'])
	c.drawString(350, 610, "Date Started: "  + ans['secondaryeducdatestarted'])
	c.drawString(350, 595, "Date Graduated: "  + ans['secondaryeducdategraduated'])

	c.drawString(50, 550, "4.b")
	c.drawString(100, 550, "Tertiary Education")
	c.rect(65, 435, 500, 100, stroke=1)
	c.drawString(100, 525, "this is me")


	c.drawString(50, 415, "4.c")
	c.drawString(100, 415, "Post-Graduate Studies")
	c.rect(65, 300, 500, 100, stroke=1)

	c.drawString(50, 280, "4.d")
	c.drawString(100, 280, "Scholastic Honors & Awards Received")
	c.rect(65, 165, 500, 100, stroke=1)

	c.drawString(50, 145, "4.e")
	c.drawString(100, 145, "Recent Scientific Publications")
	c.rect(65, 30, 500, 100, stroke=1)

	#############Page 4##############
	NGSE01(c, ans)
	c.setFillColor(black)
	c.setFont('Helvetica', 10)

	c.drawString(50, 760, "4.f")
	c.drawString(100, 760, "Recent Scientific Conference Presentations")
	c.rect(65, 645, 500, 100, stroke=1)

	c.drawString(50, 625, "4.g")
	c.drawString(100, 625, "Other Qualifications")
	c.rect(65, 510, 500, 100, stroke=1)

def EnglishProf(c, ans):
	c.setFont('Helvetica-Bold', 14)
	c.setFillColor(black)
	c.drawString(40, 490, "V. ENGLISH PROFICIENCY")
	c.setFont('Helvetica', 10)

	c.drawString(50, 470, "First Language: "  + ans['firstlang'])
	c.drawString(50, 455, "Primary Medium of Instruction")
	c.drawString(100, 440, "Secondary Level: "  + ans['mediumofinstruction2nd'])
	c.drawString(100, 425, "Tertiary Level: "  + ans['mediumofinstruction3rd'])

	c.drawString(50, 410, "Test of English Proficiency")
	c.drawString(100, 395, "Date Taken: "  + ans['engproficiencydatetaken'])
	c.drawString(100, 380, "Exam Score: "  + ans['engproficiencyscore'])

def ProgramProf(c, ans):
	c.setFont('Helvetica-Bold', 14)
	c.setFillColor(black)
	c.drawString(40, 360, "VI. PROGRAMMING PROFICIENCY")
	c.setFont('Helvetica', 10)

	c.drawString(100, 340, "Programming Language: "  + ans['lang1'])
	c.drawString(100, 325, "Programming Language: "  + ans['lang2'])
	c.drawString(100, 310, "Programming Language: "  + ans['lang3'])
	c.drawString(100, 295, "Programming Language: "  + ans['lang4'])
	c.drawString(100, 280, "Programming Language: "  + ans['lang5'])

	c.drawString(350, 340, "Level of Proficiency: "  + ans['prof1'])
	c.drawString(350, 325, "Level of Proficiency: "  + ans['prof2'])
	c.drawString(350, 310, "Level of Proficiency: "  + ans['prof3'])
	c.drawString(350, 295, "Level of Proficiency: "  + ans['prof4'])
	c.drawString(350, 280, "Level of Proficiency: "  + ans['prof5'])

	c.drawString(65, 255, "Projects/Applications")
	c.rect(65, 170, 500, 80, stroke=1)

def Essay(c, ans):
	c.setFont('Helvetica-Bold', 14)
	c.setFillColor(black)
	c.drawString(40, 150, "VII. ADMISSION ESSAY")

def References(c, ans):
	c.setFont('Helvetica-Bold', 14)
	c.setFillColor(black)
	c.drawString(40, 130, "VIII. REFERENCES")
	c.rect(65, 20, 500, 100, stroke=1)

def AppDec(c, ans):
	###########Page 5########
	NGSE01(c, ans)
	c.setFont('Helvetica-Bold', 14)
	c.setFillColor(black)
	c.drawString(40, 760, "IX. APPLICANT'S DECLARATION")
	c.setFont('Helvetica', 10)

	c.drawString(100, 740, "I declare that the information supplied in this application and the documentation supporting it are")
	c.drawString(70, 730, "true and complete. I acknowledge that the provision of incorrect information or documentation relating to my ")
	c.drawString(70, 720, "application may result in cancellation of admission or enrolment. If admitted to the National Graduate School ")
	c.drawString(70, 710, "of Engineering, I solemnly agree to abide by the rules and regulations of the College of Engineering and the ")
	c.drawString(70, 700, "University of the Philippines.")

	c.line(70, 660, 350, 660)
	c.setFont('Helvetica', 9)
	c.drawCentredString(210, 650,"Signature Over Printed Name")
	c.line(440, 660, 500, 660)
	c.drawCentredString(470, 650,"Date")

def NGSE02(c):
	c.showPage()
	c.setFont('Helvetica-Bold', 8)
	c.setFillColor(gray)
	c.drawString(58, 800, "Form NGSE-02")
	c.setFillColor(black)
	c.setFont('Helvetica', 9)
	return 790, 790

def page(c, ans):
	# NGSE02(c)
	c.setFont('Helvetica-Bold', 12)
	c.setFillColor(black)
	c.drawCentredString(306,790, 'National Graduate School of Engineering')
	c.setFont('Helvetica', 10)
	c.drawCentredString(306,778,'College of Engineering')
	c.drawCentredString(306,766,'UNIVERSITY OF THE PHILIPPINES')
	c.drawCentredString(306,754,'Diliman, Quezon City 1101 Philippines')
	c.setFont('Helvetica-Bold', 18)
	c.drawCentredString(306,720,'LETTER OF RECOMMENDATION')
	c.setFont('Helvetica-Bold', 10)
	c.drawCentredString(306,702,'NATIONAL GRADUATE SCHOOL OF ENGINEERING (NGSE) ADMISSION')
	
	c.setFont('Helvetica', 10)
	c.rect(60, 670, 136, 20, stroke=1)
	c.drawString(62, 677, "APPLICANT'S EVALUATION")
	c.setFillColor(gray)
	c.drawString(200, 677, "To be filled out by the recommender.")
	c.setFillColor(black)
	c.setFont('Helvetica-Bold', 9)
	c.drawString(60, 655, "Note to Recommender: ")
	c.setFont('Helvetica', 9)
	c.drawString(160, 655, "Any pertinent information regarding the applicant and your evaluation of the applicant's ability to")
	# c.drawString(540, 640, "N")
	c.drawString(60, 645, "undertake graduate studies and research will be held in strict confidence.")
	c.drawString(60, 620, "How long have you known applicant?")
	
	curlen = 605
	tempcur = 605
	
	tempcur, curlen = rectangle(ans['recommenderessay1'], curlen, tempcur, c)
	c.drawString(60, curlen, "In what capacity have you known the applicant?")
	tempcur-=15; curlen-=15
	if curlen <= 50:  tempcur, curlen = NGSE02(c)

	tempcur, curlen = rectangle(ans['recommenderessay2'], curlen, tempcur, c)

	c.drawString(60, curlen, "If the applicant was a student in some of your classes, what were these subjects?")
	tempcur-=15; curlen-=15
	if curlen <= 50:  tempcur, curlen = NGSE02(c)


	tempcur, curlen = rectangle(ans['recommenderessay3'], curlen, tempcur, c)

	c.drawString(60, curlen, "What do you consider as the applicant's outstanding talents or strengths in relation to graduate study")
	tempcur-=15; curlen-=15
	if curlen <= 50:  tempcur, curlen = NGSE02(c)

	tempcur, curlen = rectangle(ans['recommenderessay4'], curlen, tempcur, c)

	c.drawString(60, curlen, "What do you consider as his/her weakness or deficiencies in relation to graduate study?")
	tempcur-=15; curlen-=15
	if curlen <= 50:  tempcur, curlen = NGSE02(c)
	tempcur, curlen = rectangle(ans['recommenderessay5'], curlen, tempcur, c) 

	# ins = 'Please rate the applicant on the following characteristics in comparison with other students in the same disciplines who are known to you and who have had more or less the same amount of training and experience. Indicate size of the group with which applicant is being compared and its educational level.'

	# tempcur, curlen = rectangle(ins , curlen, tempcur)	
	tempcur-=20; curlen-=20

	c.drawString(60, curlen, "Please rate the applicant on the following characteristics in comparison with other students in the same disciplines who are")
	tempcur-=10; curlen-=10
	if curlen <= 50:  tempcur, curlen = NGSE02(c)   

	c.drawString(60, curlen, "known to you and who have had more or less the same amount of training and experience.  Indicate size of the group with")
	tempcur-=10; curlen-=10
	if curlen <= 50:  tempcur, curlen = NGSE02(c)

	c.drawString(60, curlen, "which applicant is being compared and its educational level.")
	tempcur-=20; curlen-=20
	if curlen <= 50:  tempcur, curlen = NGSE02(c)

	c.drawString(200,curlen, "Group Size: " + ans['groupSize'])
	c.drawString(290,curlen, "Education Level: " + ans['educLevel'])
	c.rect(250, curlen-2, 30, 10, stroke=1)

	c.rect(357, curlen-2, 100, 10, stroke=1)

	tempcur-=20; curlen-=20
	if curlen <= 50:  tempcur, curlen = NGSE02(c)

	c.drawString(60, curlen, "1. Intellectual ability: " + ans['recommenderq1'])
	tempcur-=10; curlen-=10
	if curlen <= 50:  tempcur, curlen = NGSE02(c)

	c.drawString(60, curlen, "2. Academic preparation for proposed field of study: " + ans['recommenderq2'])
	tempcur-=10; curlen-=10
	if curlen <= 50:  tempcur, curlen = NGSE02(c)

	c.drawString(60, curlen, "3. Motivation for proposed field of study: " + ans['recommenderq3'])
	tempcur-=10; curlen-=10
	if curlen <= 50:  tempcur, curlen = NGSE02(c)

	c.drawString(60, curlen, "4. Originality, creativity, and imagination: " + ans['recommenderq4'])
	tempcur-=10; curlen-=10
	if curlen <= 50:  tempcur, curlen = NGSE02(c)

	c.drawString(60, curlen, "5. Analytical and problem-solving ability: " + ans['recommenderq5'])
	tempcur-=10; curlen-=10
	if curlen <= 50:  tempcur, curlen = NGSE02(c)

	c.drawString(60, curlen, "6. Initiative and independence: " + ans['recommenderq6'])
	tempcur-=10; curlen-=10
	if curlen <= 50:  tempcur, curlen = NGSE02(c)

	c.drawString(60, curlen, "7. Honesty and Integrity: " + ans['recommenderq7'])
	tempcur-=10; curlen-=10
	if curlen <= 50:  tempcur, curlen = NGSE02(c)

	c.drawString(60, curlen, "8. Conscientiousness and ability to work independently: " + ans['recommenderq8'])
	tempcur-=10; curlen-=10
	if curlen <= 50:  tempcur, curlen = NGSE02(c)   

	c.drawString(60, curlen, "9. Ability to work with others: " + ans['recommenderq9'])
	tempcur-=10; curlen-=10
	if curlen <= 50:  tempcur, curlen = NGSE02(c)

	c.drawString(60, curlen, "10. Oral communication skills: " + ans['recommenderq10'])
	tempcur-=10; curlen-=10
	if curlen <= 50:  tempcur, curlen = NGSE02(c)

	c.drawString(60, curlen, "11. Written communication skills: " + ans['recommenderq11'])
	tempcur-=10; curlen-=10
	if curlen <= 50:  tempcur, curlen = NGSE02(c)

	c.drawString(60, curlen, "12. Emotional Maturity: " + ans['recommenderq12'])
	tempcur-=10; curlen-=10
	if curlen <= 50:  tempcur, curlen = NGSE02(c)   

	c.drawString(60, curlen, "13. Potential as a researcher in the discipline: " + ans['recommenderq13'])
	tempcur-=10; curlen-=10
	if curlen <= 50:  tempcur, curlen = NGSE02(c)

	c.drawString(60, curlen, "14. Potential as a teacher in the discipline: " + ans['recommenderq14'])
	tempcur-=30; curlen-=30
	if curlen <= 50:  tempcur, curlen = NGSE02(c)

	c.drawString(60, curlen, "Additional information and comments about the applicants.")
	tempcur-=15; curlen-=15
	if curlen <= 50:  tempcur, curlen = NGSE02(c)
	tempcur, curlen = rectangle(ans['recommenderessay6'], curlen, tempcur, c) 

	tempcur-=15; curlen-=15
	c.drawString(60, curlen, "I therefore " + ans['recommendation']+ " the applicant for admission to the National Graduate School of Engineering in UP Diliman.")


def rectangle(ans, curlen, tempcur, c):
	start=0; end=95
	while(start < len(ans)):
		c.drawString(60, curlen, ans[start:end])
		curlen-=10
		start = end+1
		end=end+95
	c.rect(60, curlen, 490, tempcur-curlen+10, stroke=1)
	curlen-=20 #this will be the new tempcur and curlen
	if curlen <= 50:  tempcur, curlen = NGSE02(c)

	return curlen, curlen

##############Main###################

def forms(request):
	_id = request.params['id']
	print _id
	ans = {}
	####
	q_ids = session.query(Answer.element_id).filter(Answer.user_id == _id).all()
	for q_id in q_ids:
		q = session.query(Element).filter(Element.id == q_id).one()
		a = session.query(Answer).filter(Answer.element_id == q_id).filter(Answer.user_id == _id).one()
		ans[q.name] = a.text
	_u= session.query(User).filter(User.id == _id).first()
	####
	if _u.user_type.name == 'Recommender':
		c = canvas.Canvas("form1.pdf")
		c.setLineWidth(.3)
		page(c, ans)
		c.save()
		return FileResponse('form1.pdf')
	else:
		c = canvas.Canvas("form.pdf")
		c.setLineWidth(.3)

		header(c,ans)
		ProgramOfStudy(c, ans)
		PersonalInfo(c, ans)
		EmploymentInfo(c, ans)
		AcadBg(c, ans)
		EnglishProf(c, ans)
		ProgramProf(c, ans)
		Essay(c, ans)
		References(c, ans)
		AppDec(c, ans)

		c.save()
		return FileResponse("form.pdf")
# def main(c):
#	 CREATE_FORM(c);   

# c = canvas.Canvas("form.pdf")
# c.setLineWidth(.3)
# main(c)
# c.save()



############
'''users'''

from sqlalchemy import func
def show_user(request):
	user_id = request.params['user_id']
	try:
		user = session.query(User)\
		.filter(User.id == user_id)\
		.one()
	except:
		return generateError('user id is invalid')

	d = {
		'name': user.name,
		'date_created': str(user.date_created),
		'last_modified': str(user.last_modified),
		'email': user.email,
		'user_type_id': user.user_type_id
	}


	if (user.user_type_id in [4,5]):
		# d['application_status'] = user.application_status
		attrib = session.query(ApplicantAttribute).filter(ApplicantAttribute.applicant_id==user_id).one()
		d['validation_status'] = attrib.validation_status
		d['application_status'] = attrib.application_status
		d['answered_pos'] = attrib.answered_pos

		d['level'] = attrib.level
		d['program'] = attrib.program
		d['program_type'] = attrib.program_type
		d['student_type'] = attrib.student_type
		d['choice_1'] = attrib.choice_1
		d['choice_2'] = attrib.choice_2
		d['choice_3'] = attrib.choice_3
		d['adviser'] = attrib.adviser
		d['start_of_study'] = attrib.start_of_study
		d['year'] = attrib.year
		d['other_scholarship'] = attrib.other_scholarship
		d['other_scholarship_name'] = attrib.other_scholarship_name

		# get recommender info
		
		d['recommenders'] = []
		if (attrib.recommender_a is None or attrib.recommender_b is None or attrib.recommender_c is None):
			for i in range(3):
				d['recommenders'].append({'name': 'Not yet assigned'})
		else:
			for recommender in [(attrib.recommender_a, attrib.rec_a), (attrib.recommender_b, attrib.rec_b), (attrib.recommender_c, attrib.rec_c)]:
				info = {
					'id': recommender[0],
					'name': recommender[1].name,
					'status': True
				}

				category_statuses = session.query(CategoryStatus)\
					.filter(CategoryStatus.user_id == recommender[0])\
					.all()

				for category_status in category_statuses:
					if not category_status.status:
						info['status'] = False
						break

				d['recommenders'].append(info)

	if (user.user_type_id in [3,4,5]):
		d['submitted'] = user.submitted

		categories = session.query(CategoryStatus)\
			.filter(CategoryStatus.user_id == user_id)\
			.all()

		d['answered'] = []

		for category in categories:
			d['answered'].append({
				'id': category.id,
				'category_id': category.category_id,
				'status': category.status	
			})

		answers = session.query(Answer)\
			.filter(Answer.user_id == user_id)\
			.all()

		d['answers'] = []

		for answer in answers:
			d['answers'].append({
				'id': answer.id,
				'category_id': answer.element.category_id,
				'element_id': answer.element_id,
				'name': answer.text
			})

	return d

def update_user(request):
	token = request.authorization[1]
	payload = decode(token)
	user_id = payload['sub']

	user = session.query(User)\
		.filter(User.id == user_id)\
		.one()

	submitted = request.params.get('submitted', None)
	password = request.params.get('password', None)
	appstat = request.params.get('application_status', None)
	valstat = request.params.get('validation_status', None)

	if not submitted is None:
		user.submitted = submitted
		session.commit()
		return generateSuccess('user submission successful')

	if not password is None:
		user.password = bcrypt.hashpw(password, bcrypt.gensalt())
		session.commit()
		return generateSuccess('password successfully changed')

	if not appstat is None:
		user.application_status = appstat
		session.commit()
		return generateSuccess('application status successfully changed')

	if not valstat is None:
		user.validation_status = valstat
		session.commit()
		return generateSuccess('validation status successfully changed')

	user_attribs = session.query(ApplicantAttribute)\
		.filter(ApplicantAttribute.applicant_id == user_id)\
		.one()

	attribs = [
		'level',
		'program',
		'program_type',
		'student_type',
		'choice_1',
		'choice_2',
		'choice_3',
		'adviser',
		'start_of_study',
		'year',
		'other_scholarship',
		'other_scholarship_name'
	]

	for key in attribs:
		value = request.params.get('user[{}]'.format(key))
		if (key == 'level'):
			user_attribs.level = value
		if (key == 'program'):
			user_attribs.program = value
		if (key == 'program_type'):
			user_attribs.program_type = value
		if (key == 'student_type'):
			user_attribs.student_type = value
		if (key == 'choice_1'):
			user_attribs.choice_1 = value
		if (key == 'choice_2'):
			user_attribs.choice_2 = value
		if (key == 'choice_3'):
			user_attribs.choice_3 = value
		if (key == 'adviser'):
			user_attribs.adviser = value
		if (key == 'start_of_study'):
			user_attribs.start_of_study = value
		if (key == 'year'):
			user_attribs.year = value
		if (key == 'other_scholarship'):
			user_attribs.other_scholarship = value
		if (key == 'other_scholarship_name'):
			user_attribs.other_scholarship_name = value

	user_attribs.answered_pos = True

	session.commit()

	return {'success': True}










################################################################

def get_forms(request):
	d = []
	for f in session.query(Form):
		started = is_past(str(f.date_start))
		ended = is_past(str(f.date_end))

		status = 'idle' if (not started) else ( 'expired' if (ended) else 'ongoing' )

		d.append({
			'id': int(f.id),
			'name': f.name,
			'user': f.form_type.user_type_id,
			'date_start': str(f.date_start),
			'date_end': str(f.date_end),
			'status': status
		})
	return d

def create_form(request):
	# we need name, form type id, date start, date end
	name = request.params['name']
	form_type_id = request.params['form_type_id']
	date_start = request.params['date_start']
	date_end = request.params['date_end']

	form = Form(
		name=name,
		date_start=date_start,
		date_end=date_end,
		form_type_id=form_type_id
		)
	session.add(form)
	session.commit()

	return {'success': True}

def delete_form(request):
	_id = request.params['id']

	form = session.query(Form)\
	.filter(Form.id == _id)\
	.one()

	session.delete(form)
	session.commit()

	return {'success': True}

def show_form(request):
	form_id = request.params.get('form_id')

	if form_id is None:
		return generateError('invalid form id')

	try:
		form = session.query(Form)\
			.filter(Form.id == form_id)\
			.one()
	except:
		return generateError('Invalid form id')

	d = {
		'name': form.name,
		'date_created': str(form.date_created),
		'last_modified': str(form.last_modified),
		'date_start': str(form.date_start),
		'date_end': str(form.date_end),
		'form_type_id': form.form_type_id,
		'user_type_id': form.form_type.user_type_id,
		'page_sequence': form.form_type.page_sequence
	}

	return d

def update_form(request):
	id = request.params['id']

	form = session.query(Form)\
	.filter(Form.id == id)\
	.one()

	name = request.params.get('name', None)
	if name is not None:
		form.name = name

	date_start = request.params.get('date_start', None)
	if date_start is not None:
		form.date_start = date_start

	date_end = request.params.get('date_end', None)
	if date_end is not None:
		form.date_end = date_end

	form_type_id = request.params.get('form_type_id', None)
	if form_type_id is not None:
		form.form_type_id = form_type_id

	session.commit()

	return generateSuccess('Success')

def get_form_types(request):
	d = []
	for ft in session.query(FormType):
		d.append({
			'id': ft.id,
			'name': ft.name,
			'page_sequence': ft.page_sequence,
			'date_created': str(ft.date_created),
			'last_modified': str(ft.last_modified)
		})
	return d

################################################################

def get_categories(request):
	form_id = request.params.get('form_id')

	form = session.query(Form)\
		.filter(Form.id == form_id)\
		.one()

	result = []

	for category in session.query(Category).join(Category.form_type, aliased=True).filter_by(id = form.form_type_id):
		result.append({
			'id': category.id,
			'name': category.name
		})

	return result

def show_category(request):
	category_id = request.params.get('category_id')

	category = session.query(Category)\
		.filter(Category.id == category_id)\
		.one()

	d = {
		'id': category.id,
		'name': category.name,
		'date_created': str(category.date_created),
		'last_modified': str(category.last_modified),
		'form_type_ids': []
	}

	associations = session.query(form_category_association)\
		.filter(form_category_association.c.categories_id == category.id)\
		.all()

	for association in associations:
		d['form_type_ids'].append(association.form_types_id)

	return d



################################################################


def get_elements(request):
	category_id = request.params.get('category_id')
	result = []

	for element in session.query(Element).filter(Element.category_id == category_id):
		q = {
			'id': int(element.id),
			'name': element.name,
			'text': element.text,
			'klass': element.klass,
			'kind': element.kind,
			'width': word(element.width)
		}
 
		if (element.klass == 'question'):
			q['required'] = element.required

		if (element.choices):
			q['choices'] = element.choices

		if (element.default):
			q['default'] = element.default
		
		result.append(q)

	return result

################################################################

# def get_answers(request): # old
# 	user_id = request.params.get('user_id')
# 	category_id = request.params.get('category_id')
# 	result = []

# 	for answer in session.query(Answer).filter(Answer.user_id == user_id).join(Answer.element, aliased=True).filter_by(category_id=category_id):
# 		result.append({
# 			'id': answer.id,
# 			'text': answer.text,
# 			'element_id': answer.element_id
# 		})
	
# 	return result

def get_answers(request): # new
	result = []

	for answer in session.query(Answer):
		result.append({
			'id': answer.id,
			'text': answer.text,
			'element_id': answer.element_id,
			'user_id': answer.user_id
		})
	
	return result

def update_answer(request):
	user_id = request.params.get('user_id')
	category_id = request.params.get('category_id')
	data = request.params.get('data')
	length = request.params.get('length')

	try:
		user = session.query(User).filter(User.id == user_id).one()
	except:
		return generateError('User id invalid')

	# change category status to answered
	category_status = session.query(CategoryStatus)\
		.filter(CategoryStatus.user_id == user_id)\
		.filter(CategoryStatus.category_id == category_id)\
		.one()

	category_status.status = True
	session.commit()

	for i in range(int(length)):
		answer_id = request.params.get('data[{}][id]'.format(i))
		text = request.params.get('data[{}][text]'.format(i))
		
		answer = session.query(Answer)\
			.filter(Answer.user_id == user_id)\
			.filter(Answer.id == answer_id)\
			.one()
		answer.text = text
	
		e = session.query(Element).filter(Element.id == answer.element_id).one()
		# if answer.element_id in [70, 71, 75, 76, 80, 81] and text != '':
		if (e.text == "Recommender Name" or e.text == "Recommender E-mail" ) and (text != ""):	
			# if hindi pa existing create a new recommender
			# if answer.element_id in [70, 75, 80]:
			if e.text == "Recommender Name":
				recName = text;

			# elif answer.element_id in [71, 76, 81]:
			elif e.text == "Recommender E-mail":
				attr = session.query(ApplicantAttribute)\
					.filter(ApplicantAttribute.applicant_id == user_id).one()

				#### edit by daisy may 31
				# generated_password = 'password'
				generated_password = password_generator()
				file = open("passwords.txt", 'a')
				file.write("email: " + text + " , password: " + generated_password + "\n")
				file.close()
				####

				password = bcrypt.hashpw(generated_password, bcrypt.gensalt())

				rec = User(name=recName, email=text, password=password, user_type_id='3')
				# session.add(rec)
				# session.commit()

				print answer.element_id
				success = False

				# if answer.element_id == 71 and attr.recommender_a == None:
				if e.name == "rec1email" and attr.recommender_a == None:	
					session.add(rec)
					session.commit()
					attr.recommender_a = rec.id
					session.commit()
					success = True
				# elif answer.element_id == 76 and attr.recommender_b == None:
				elif e.name == "rec2email" and attr.recommender_b == None:
					session.add(rec)
					session.commit()
					attr.recommender_b = rec.id
					session.commit()
					success = True
				# elif answer.element_id == 81 and attr.recommender_c == None:
				elif e.name == "rec3email" and attr.recommender_c == None:				
					session.add(rec)
					session.commit()
					attr.recommender_c = rec.id
					session.commit()
					success = True
				if(success):
					send_recommender_email(request.mailer, rec.name, user.name, text, generated_password)
					form_type = session.query(FormType).filter(FormType.user_type_id == rec.user_type_id).one()
					category_ids = form_type.page_sequence
					questions = []
					for category_id in category_ids:
						toadd = session.query(Element).filter(Element.klass == 'question').filter(Element.category_id == category_id).all()
						for entry in toadd:
							questions.append(entry)

					for question in questions:
						answer = Answer(text='', element_id=question.id, user_id=rec.id)
						session.add(answer)
						session.commit()			

								# initialize all status of categories_answered to False
					for category_id in category_ids:
						category_status = CategoryStatus(user_id=rec.id, category_id=category_id)
						session.add(category_status)

					session.commit()

		########
	session.commit()
	return generateSuccess('Successfully updated answer')




	# db_ans = session.query(Answer)\
	# 		.filter(Answer.element_id == q_id)\
	# 		.filter(Answer.user_id == user_id)\
	# 		.all()

	# if(db_ans == []):
	# 	try:
	# 		answer = Answer(name=curr_ans, element_id=q_id, user_id=user_id)
	# 		session.add(answer)
	# 		session.commit()
	# 		# return{'message': 'Answer saved', 'success':True}
	# 	except:
	# 		return{'message': 'Smth went wrong', 'success': False}
	# else:
	# 	try:
	# 		# update lang here
	# 		answer = session.query(Answer)\
	# 				.filter(Answer.element_id == q_id)\
	# 				.filter(Answer.user_id == user_id)\
	# 				.first()
	# 		answer.name = curr_ans
	# 		session.commit()
	# 		# return{'message': 'Answer saved', 'success':True}
	# 	except:
	# 		return{'message': 'Smth went wrong', 'success':False}
	# return{'message': 'Answer saved', 'success':True}

# def view_answer(request):
def show_answer(request):
	user_id = request.params.get('user_id')
	category_id = request.params.get('category_id')

	if user_id is None or category_id is None:
		return generateError('invalid user id or category id')

	try:
		u = session.query(User).filter(User.id == user_id).one()
	except:
		return generateError('invalid user id')

	try:
		c = session.query(Category).filter(Category.id == category_id).one()
	except:
		return generateError('invalid category id')

	result = []

	answers = session.query(Answer).filter(Answer.user_id == user_id).join(Answer.element, aliased=True).filter_by(category_id=category_id)

	for answer in answers:
		result.append({
			'id': answer.id,
			'text': answer.text,
			'date_created': str(answer.date_created),
			'last_modifed': str(answer.last_modified),
			'element_id': answer.element_id
		})

	return result

def get_users(request):
	d = []
	for u in session.query(User):
		if u.user_type.name == "ERDT Applicant" or u.user_type.name == "Non-ERDT Applicant":
			_u = session.query(ApplicantAttribute).filter(ApplicantAttribute.applicant_id == u.id).first()
			rec_a = session.query(User).filter(User.id == _u.recommender_a).all()
			rec_b = session.query(User).filter(User.id == _u.recommender_b).all()
			rec_c = session.query(User).filter(User.id == _u.recommender_c).all()

			rec = [rec_a, rec_b, rec_c]			
			for r in rec:
				if r != []:
					rec[rec.index(r)] = r[0].name
				else:
					rec[rec.index(r)] = "None"
			d.append({
				'id': int(u.id),
				'name': u.name,
				'email':u.email,
				'user_type': u.user_type.name,
				'application_status': _u.application_status,
				'validation_status': _u.validation_status,
				'recommender1': rec[0],
				'recommender2': rec[1],
				'recommender3': rec[2],
				'date_created': str(u.date_created),
				'last_modified': str(u.last_modified)
				})
		else:
			d.append({
				'id': int(u.id),
				'name': u.name,
				'email':u.email,
				'user_type': u.user_type.name,
				'date_created': str(u.date_created),
				'last_modified': str(u.last_modified)
			})   
	return d

def verify_user(request):
	token = request.params.get('token', None)

	if token is None:
		return generateError('Token is missing', {'expired': False})

	try:
		payload = decode(token)
	except jwt.ExpiredSignatureError:
		return generateError('Token has expired', {'expired': True})
	except:
		return generateError('Token is invalid', {'expired': False})

	return generateSuccess('Token is valid', {'expired': False})

def login_user(request):
	email = request.params.get('email', None)
	password = request.params.get('password', None)

	if email is None or password is None:
		return generateError('Invalid email and password combination')

	try:
		user = session.query(User).filter(User.email == email).one()
		pwd = bcrypt.hashpw(password.encode('UTF_8'), user.password.encode('UTF_8'))

		if (pwd != user.password):
			return generateError('Invalid email and password combination')
	except MultipleResultsFound:
		users = session.query(User).filter(User.email == email).all()
		user = None
		for u in users:
			pwd = bcrypt.hashpw(password.encode('UTF_8'), u.password.encode('UTF_8'))
			if (pwd == u.password):
				user = u
				break
		if user == None:  
			return generateError('Invalid email and password combination')

	except NoResultFound:
		return generateError('Invalid email and password combination')


	return generateSuccess('Welcome, {}!'.format(user.name), {'token': generateToken(user)})

from email.utils import parseaddr

def create_user(request):
	# check for required params, return error if incomplete

	email = request.params.get('email', None)
	last = request.params.get('last', None)
	given = request.params.get('given', None)
	middlemaiden = request.params.get('middlemaiden', None)
	level = request.params.get('level', None)
	fullname = '{} {}'.format(given, last)

	parsed = parseaddr(email)

	if parsed[1] == "":
		return generateError('Invalid email')
	########## 
	#EDIT: may 31 - daisy
	# generated_password = 'password'

	generated_password = password_generator()

	#just for debugging purposes. will delete these lines eventually

	file = open("passwords.txt", 'a')
	file.write("email: " + email + " , password: " + generated_password + "\n")
	file.close()

	password = bcrypt.hashpw(generated_password, bcrypt.gensalt())

	if email is None or last is None or given is None or middlemaiden is None:
		return generateError('Field is missing')

	# check if user is not recommender email is linked to an account
	u = session.query(User).filter(User.email == email).all()
	if (level != 3 and len(u) > 0):
		return generateError('E-mail is already in use')

	try:
		if level is None:
			u = User(name=fullname, email=email, password=password)
		else:
			u = User(name=fullname, email=email, password=password, user_type_id=int(level))
	except:
		return generateError('Something weird happened!')

	send_credentials_email(request.mailer, given, email, generated_password)

	session.add(u)
	session.commit()

	if int(level) in [3,4,5]:

		#######
		# add a row in ApplicantAttribute Table
		if level == '4':
			row = ApplicantAttribute(scholarship = False, applicant_id=u.id)
		elif level == '5':
			row = ApplicantAttribute(scholarship = True, applicant_id=u.id)
		
		if int(level) in [4,5]:
			session.add(row)
			session.commit()
		#######

		# create answer} 
		form_type = session.query(FormType).filter(FormType.user_type_id == u.user_type_id).one()
		# forms = session.query(Form).filter(Form.form_type_id == form_type.id).all()
		# for f in forms:
		# 	started = is_past(str(f.date_start))
		# 	ended = is_past(str(f.date_end))

		# 	status = 'idle' if (not started) else ( 'expired' if (ended) else 'ongoing' )

		# 	if (status is 'ongoing'):
		# 		form = f
		# 		break
		category_ids = form_type.page_sequence
		questions = []

		for category_id in category_ids:
			toadd = session.query(Element).filter(Element.klass == 'question').filter(Element.category_id == category_id).all()
			for entry in toadd:
				questions.append(entry)

		for question in questions:
			answer = Answer(text='', element_id=question.id, user_id=u.id)
			if question.default:
				answer.text = question.default
			session.add(answer)
			session.commit()

		# initialize all status of categories_answered to False
		for category_id in category_ids:
			category_status = CategoryStatus(user_id=u.id, category_id=category_id)
			session.add(category_status)

		session.commit()
 
	return generateSuccess('Welcome, {}!'.format(fullname), {'token': generateToken(u)})

def delete_user(request):
	'''
	input id of user accessing endpoint, id of user to delete, type of user
	input step number for testing
	'''

	step = int(request.params.get('step', 0)) # variable for testing
	user_id = request.params.get('user_id', None)
	_id = request.params.get('id', None)

	if user_id is None or _id is None: # user_id was not passed
		return generateError('Required field is missing')

	try:
		user_id = int(user_id)
	except ValueError: # user_id not an integer
		return generateError('user_id is invalid')

	if user_id < 1 or user_id > 2147483647: # user_id beyond range
		return generateError('user_id is out of bounds')

	try:
		_id = int(_id)
	except ValueError: # id not an integer
		return generateError('id is invalid')

	if _id < 1 or _id > 2147483647:
		return generateError('id is out of bounds')

	try:
		user = session.query(User).filter(User.id == user_id).one()
	except NoResultFound: # user_id not found in database 
		return generateError('User accessing does not exist')

	user_type = user.user_type_id

	if ((user_type != 1) and (user_id != _id)): # not admin deleting different id
		return generateError('Unauthorized')

	if ((user_type == 1) and (user_id == _id)): # admin deleting admin id
		return generateError('Cannot delete admin account')

	try:
		other_user = session.query(User).filter(User.id == _id).one()
	except NoResultFound: # id not found in database
		return generateError('User ')

	if step == 5:
		return {'message': 'other user exists'}


	# return {'message': 'oh no', 'success': False}

def update_application_status(request):
	#if admin
	user_id = request.params['user_id']
	status = request.params['a_status']

	app = session.query(ApplicantAttribute).filter(ApplicantAttribute.applicant_id == user_id).first()

	if app == None: return{'message': 'user is not an applicant', 'success':False}
	app.application_status= status
	session.commit()
	return {'message': 'Status successfully updated', 'success': True}


#returns application and validation status of applicant
''' edit: this is already in show_user function
def view_status(request): 
	user_id = request.params['user_id']
	app = session.query(ApplicantAttribute).filter(ApplicantAttribute.applicant_id == user_id).first()

	if app == None: return{'message': 'user is not an applicant', 'success':False}
	user = session.query(User).filter(User.id == user_id).first()					

	return{ 'name': user.name, 'application status': app.application_status, 'validation_status': app.validation_status}
'''
def update_validation_status(request):
	user_id = request.params['user_id']
	status = request.params['v_status'] # complete, incomplete, not yet submitted
	app = session.query(ApplicantAttribute).filter(ApplicantAttribute.applicant_id == user_id).first()
	
	if app == None: return{'message': 'user is not an applicant', 'success':False}
	app.validation_status= status
	session.commit()
	return {'message': 'Validation status successfully updated', 'success': True}


def reset_database(request):
	# if admin

	# problem: does not delete the id sequence
	for answer in session.query(Answer).all():
		session.delete(answer)
	for attrib in session.query(ApplicantAttribute).all():
		session.delete(attrib)
	for status in session.query(CategoryStatus).all():
		session.delete(status)
	for user in session.query(User).filter(User.user_type_id > 2).all():
		session.delete(user)

	session.commit()
	return {'success': True}
