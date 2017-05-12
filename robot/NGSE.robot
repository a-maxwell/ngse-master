*** Settings ***
Resource          resources.robot

*** Variables ***
${SUCCESS}        Succesfully logged in

*** Test Cases ***
Clear Database
    Open Browser    http://localhost:6543/v1/delete_all    ${BROWSER}
    Reset Database
    [Teardown]    Close Browser

Invalid Login
    [Setup]    Setup
    [Template]    Login with invalid credentials should fail
    mfmayol@up.edu.ph    password
    yes    huhuhuhu
    no    huhuhu
    [Teardown]    Close Browser

Succesful Non-ERDT Reg
    [Setup]    Setup
    [Template]    Non-ERDT Reg with valid info should pass
    Michael Pio    Fortuno    Mayol    mfmayol@up.edu.ph
    Gerard    Borja    Montemayor    gbmontemayor@up.edu.ph
    [Teardown]    Close Browser

Successful ERDT Reg
    [Setup]    Setup
    [Template]    ERDT Reg with valid info should pass
    Je Marie    Alfaro    Apolinario    jaapolinario@up.edu.ph
    Bernadette    Bitong    Misa    bbmisa@up.edu.ph
    [Teardown]    Close Browser

Unsuccessful Reg
    [Setup]    Setup
    [Template]    Reg with invalid info should fail
    Michael Pio    Fortuno    Mayol    mfmayol@up.edu.ph
    Gerard    Borja    Montemayor    gbmontemayor@up.edu.ph
    [Teardown]    Close Browser

Valid Login
    [Setup]    Setup
    [Template]    Login with valid credentials should pass
    mfmayol@up.edu.ph    ${DEFAULT PASSWORD}
    gbmontemayor@up.edu.ph    ${DEFAULT PASSWORD}
    jaapolinario@up.edu.ph    ${DEFAULT PASSWORD}
    bbmisa@up.edu.ph    ${DEFAULT PASSWORD}
    [Teardown]    Close Browser

Answer Program of Study
    [Setup]    Setup
    [Template]    Fill up Program of Study with valid info should pass
    mfmayol@up.edu.ph    Master of Science    CE    Non Thesis    Full Time    First Semester    2017-2018
    ...    Yes    Elif Scholarship
    bbmisa@up.edu.ph    Doctor of Philosophy    ChE    Non Thesis    Part Time    Second Semester    2018-2019
    ...    Yes    Else Scholarship
    [Teardown]    Close Browser

Check Program of Study

*** Keywords ***
Login with invalid credentials should fail
    [Arguments]    ${username}    ${password}
    Login    ${username}    ${password}
    Location Should Be    http://${HOST}/auth

Non-ERDT Reg with valid info should pass
    [Arguments]    ${first}    ${middlemaiden}    ${last}    ${email}
    Register    ${first}    ${middlemaiden}    ${last}    ${email}
    Location Should Be    http://${HOST}/
    [Teardown]    Click Element    id=logout

ERDT Reg with valid info should pass
    [Arguments]    ${first}    ${middlemaiden}    ${last}    ${email}
    Click Element    name=scholarship
    Register    ${first}    ${middlemaiden}    ${last}    ${email}
    Location Should Be    http://${HOST}/
    [Teardown]    Click Element    id=logout

Login with valid credentials should pass
    [Arguments]    ${username}    ${password}
    Login    ${username}    ${password}
    Location Should Be    http://${HOST}/
    [Teardown]    Click Element    id=logout

Reg with invalid info should fail
    [Arguments]    ${first}    ${middlemaiden}    ${last}    ${email}
    Register    ${first}    ${middlemaiden}    ${last}    ${email}
    Location Should Be    http://${HOST}/auth

Login and go to Program of Study
    [Arguments]    ${email}
    Login    ${email}    ${DEFAULT PASSWORD}
    Click Element    id=application
    Click Element    id=program-of-study

Fill up Program of Study with valid info should pass
    [Arguments]    ${email}    ${1}    ${2}    ${3}    ${4}    ${5}
    ...    ${6}    ${7}    ${8}
    Login and go to Program of Study    ${email}
    Click Element    xpath=(//div[contains(@class, 'button') and text() = '${1}'])
    Click Element    xpath=(//div[contains(@class, 'button') and text() = '${2}'])
    Click Element    xpath=(//div[contains(@class, 'button') and text() = '${3}'])
    Click Element    xpath=(//div[contains(@class, 'button') and text() = '${4}'])
    Click Element    xpath=(//div[contains(@class, 'button') and text() = '${5}'])
    Input Text    name=year    ${6}
    Click Element    xpath=(//div[contains(@class, 'button') and text() = '${7}'])
    Input Text    model=user.other_scholarship_name    ${8}
    Click Element    id=submit
    Location Should Be    http://${HOST}/application
    ${result} =    Get Text    id=program-of-study-text
    Should Be Equal As String    ${result}    Answered
