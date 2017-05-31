*** Settings ***
Documentation     A resource file with reusable keywords and variables.
...
...               The system specific keywords created here form our own
...               domain specific language. They utilize keywords provided
...               by the imported Selenium2Library.
Library           ExtendedSelenium2Library
Library           Dialogs

*** Variables ***
${HOST}           localhost:6543/#!
${BROWSER}        Chrome
${LOGIN URL}      /auth
${REGISTRATION URL}    /auth
${APPLICATION STATUS URL}    /application
${DEFAULT PASSWORD}    password

*** Keywords ***
Login
    [Arguments]    ${email}
    Input Text    model=login.email    ${email}
    ${password} =    Get Value From User    Input password    hidden=yes
    Input Text    model=login.password    ${password}
    Click Element    name=login

Register
    [Arguments]    ${first}    ${middlemaiden}    ${last}    ${email}
    Input Text    model=registration.last    ${last}
    Input Text    model=registration.given    ${first}
    Input Text    model=registration.middlemaiden    ${middlemaiden}
    Input Text    model=registration.email    ${email}
    Click Element    name=register

Reset Database
    Go To    http://${HOST}/v1/delete_all

Setup
    [Arguments]    ${url}
    Open Browser    ${url}    ${BROWSER}
