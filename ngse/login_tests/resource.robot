*** Settings ***
Documentation     A resource file with reusable keywords and variables.
...
...               The system specific keywords created here form our own
...               domain specific language. They utilize keywords provided
...               by the imported Selenium2Library.
Library           Selenium2Library

*** Variables ***
${SERVER}         localhost:6543
${BROWSER}        Firefox
${DELAY}          0
${VALID USER}     ngse@coe.upd.edu.ph
${VALID PASSWORD} ngse
${LOGIN URL}      http://${SERVER}/#!/auth
${WELCOME URL}    http://${SERVER}/#!/application
${ERROR URL}      http://${SERVER}/#!/auth

*** Keywords ***
Open Browser To Login Page
    Open Browser    ${LOGIN URL}    ${BROWSER}
    Maximize Browser Window
    Set Selenium Speed    ${DELAY}
    Login Page Should Be Open

Login Page Should Be Open
    Title Should Be    National Graduate School of Engineering

Go To Login Page
    Go To    ${LOGIN URL}
    Login Page Should Be Open

Input Username
    [Arguments]    ${username}
    Input Text    email    ${username}

Input Password
    [Arguments]    ${password}
    Input Text    password    ${password}

Submit Credentials  
    Click Button    ui button

Welcome Page Should Be Open
    Location Should Be    ${WELCOME URL}
    Title Should Be    Welcome Page
