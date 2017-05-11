*** Settings ***
Documentation     A resource file with reusable keywords and variables.
...
...               The system specific keywords created here form our own
...               domain specific language. They utilize keywords provided
...               by the imported Selenium2Library.
Library           ExtendedSelenium2Library

*** Variables ***
${HOST}                     localhost:6543/#!
${BROWSER}                  Chrome
${LOGIN URL}                /auth
${REGISTRATION URL}         /auth
${APPLICATION STATUS URL}   /application

*** Keywords ***
Login
    [Arguments]     ${username}             ${password}
    Input Text      model=login.email       ${username}
    Input Text      model=login.password    ${password}
    Click Element   name=login

Register
    [Arguments]     ${first}    ${middlemaiden}     ${last}     ${email}
    Input Text      model=login.last                ${last}
    Input Text      model=login.first               ${first}
    Input Text      model=login.middlemaiden        ${middlemaiden}
    Input Text      model=login.email               ${email}
    Click Element   name=register

Register ERDT
    [Arguments]     ${first}    ${middlemaiden}     ${last}     ${email}
    Register        ${first}    ${middlemaiden}     ${last}     ${email}
    Click Element   name=scholarship

Register NonERDT
    [Arguments]     ${first}    ${middlemaiden}     ${last}     ${email}
    Register        ${first}    ${middlemaiden}     ${last}     ${email}

Reset Database
    Go To   ${HOST}/v1/delete_all