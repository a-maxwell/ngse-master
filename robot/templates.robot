*** Settings ***
Resource          resources.robot

*** Variables ***
${SUCCESS}	Succesfully logged in

*** Keywords ***
Login with invalid credentials should fail
	[Arguments]		${username}		${password}
	Login			${username}		${password}
	${message} = 	Get Text		id=message-text
	${result} =		Should Be Equal As Strings	${message}	${SUCCESS}
	Should Not Be True	${result}

*** Test Cases ***
Invalid Login
	[Template]	Login with invalid credentials should fail
	mfmayol@up.edu.ph	thisisapassword
	yes					huhuhuhu