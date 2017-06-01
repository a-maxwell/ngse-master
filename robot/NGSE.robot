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
    [Setup]    Setup    ${HOST}
    [Template]    Login with invalid credentials should fail
    yes
    no
    [Teardown]    Close Browser

Succesful Non-ERDT Reg
    [Setup]    Setup    ${HOST}
    [Template]    Non-ERDT Reg with valid info should pass
    Michael Pio    Fortuno    Mayol    mfmayol@up.edu.ph
    [Teardown]    Close Browser

Successful ERDT Reg
    [Setup]    Setup    ${HOST}
    [Template]    ERDT Reg with valid info should pass
    Je Marie    Alfaro    Apolinario    bmicons360@gmail.com
    [Teardown]    Close Browser

Unsuccessful Reg
    [Setup]    Setup    ${HOST}
    [Template]    Reg with invalid info should fail
    Michael Pio    Fortuno    Mayol    mfmayol@up.edu.ph
    [Teardown]    Close Browser

Check GMail
    [Setup]
    [Template]    Check GMail Account for confirmation E-mail
    mfmayol@up.edu.ph
    bmicons360@gmail.com
    [Teardown]

Valid Login
    [Setup]    Setup    ${HOST}
    [Template]    Login with valid credentials should pass
    mfmayol@up.edu.ph
    bmicons360@gmail.com
    [Teardown]    Close Browser

Answer Program of Study Non-Thesis Other Scholarship
    [Setup]    Setup    ${HOST}
    [Template]    Fill up Program of Study Non-Thesis Other Scholarship
    mfmayol@up.edu.ph    Master of Science    MSE    Non Thesis    Full Time    First Semester    2017-2018
    ...    Yes    Other Scholarship
    [Teardown]    Close Browser

Answer Program of Study Thesis ERDT
    [Setup]    Setup    ${HOST}
    [Template]    Fill up Program of Study Thesis ERDT
    bmicons360@gmail.com    Doctor of Philosophy    CE    Thesis    Part Time    Water Resources    Geotechnical
    ...    Transportation    Second Semester    2018-2019    No
    [Teardown]    Close Browser

Fill Up Application Form
    [Setup]    Setup    ${HOST}
    Login    mfmayol@up.edu.ph
    Click Element    id=application
    Click Element    id=personal-information
    Input Text    name=lastname    Mayol
    Input Text    name=givenname    Michael Pio
    Input Text    name=middlename    Fortuno
    Click Element    xpath=(//div[contains(concat(' ', @class, ' '), ' dropdown ')])[1]
    Click Element    xpath=(//div[text() = 'Male'])
    Click Element    name=birthdate
    Click Element    xpath=(//span[text() = 'June 2017'])
    Click Element    xpath=(//span[text() = '2017'])
    Click Element    xpath=(//span[contains(concat(' ', @class, ' '), ' prev ')])[1]
    Click Element    xpath=(//span[contains(concat(' ', @class, ' '), ' prev ')])[1]
    Click Element    xpath=(//td[text() = '1997'])
    Click Element    xpath=(//td[text() = 'May'])
    Click Element    xpath=(//td[text() = '22'])
    Input Text    name=birthplace    Cebu
    Input Text    name=civilstatus    Single
    Click Element    xpath=(//div[contains(concat(' ', @class, ' '), ' dropdown ')])[2]
    Click Element    xpath=(//div[contains(concat(' ', @class, ' '), ' item ') and text() = 'Philippines'])[1]
    Input Text    name=citizenship    Filipino
    Input Text    xpath=(//textarea[contains(concat(' ', @title, ' '), ' currentaddress ')])[1]    Visayas Avenue, VASRA, Quezon City
    Input Text    name=currentpostal    1128
    Click Element    xpath=(//div[contains(concat(' ', @class, ' '), ' dropdown ')])[3]
    Click Element    xpath=(//div[contains(concat(' ', @class, ' '), ' item ') and text() = 'Philippines'])[2]
    Input Text    xpath=(//textarea[contains(concat(' ', @title, ' '), ' permanentaddress ')])[1]    Visayas Avenue, VASRA, Quezon City
    Input Text    name=permanentpostal    1128
    Click Element    xpath=(//div[contains(concat(' ', @class, ' '), ' dropdown ')])[4]
    Click Element    xpath=(//div[contains(concat(' ', @class, ' '), ' item ') and text() = 'Philippines'])[3]
    Input Text    name=telephonenumber    9274122
    Input Text    name=faxnumber    9274122
    Input Text    name=emailaddress    mfmayol@up.edu.ph
    Input Text    name=fathersname    Bernabe Mayol
    Input Text    name=mothersname    Gia Maria Mayol
    Input Text    name=emergencyname    Gia Maria Mayol
    Input Text    xpath=(//textarea[contains(concat(' ', @title, ' '), ' emergencyaddress ')])[1]    Visayas Avenue, VASRA, Quezon City
    Input Text    name=emergencyrelationship    Mother
    Input Text    name=emergencynumber    9274122
    Click Element    xpath=(//button)[1]
    Sleep    2
    Location Should Be    http://${HOST}/application
    ${result} =    Get Text    id=personal-information-text
    Should Be Equal As Strings    ${result}    Answered
    [Teardown]    Close Browser

*** Keywords ***
Login with invalid credentials should fail
    [Arguments]    ${username}
    Login    ${username}
    Location Should Be    http://${HOST}/auth

Non-ERDT Reg with valid info should pass
    [Arguments]    ${first}    ${middlemaiden}    ${last}    ${email}
    Register    ${first}    ${middlemaiden}    ${last}    ${email}
    Location Should Be    http://${HOST}/application
    [Teardown]    Click Element    id=logout

ERDT Reg with valid info should pass
    [Arguments]    ${first}    ${middlemaiden}    ${last}    ${email}
    Click Element    name=scholarship
    Register    ${first}    ${middlemaiden}    ${last}    ${email}
    Location Should Be    http://${HOST}/application
    [Teardown]    Click Element    id=logout

Login with valid credentials should pass
    [Arguments]    ${username}
    Login    ${username}
    Location Should Be    http://${HOST}/application
    [Teardown]    Click Element    id=logout

Reg with invalid info should fail
    [Arguments]    ${first}    ${middlemaiden}    ${last}    ${email}
    Register    ${first}    ${middlemaiden}    ${last}    ${email}
    Location Should Be    http://${HOST}/auth

Login and go to Program of Study
    [Arguments]    ${email}
    Login    ${email}
    Click Element    id=application
    Click Element    id=program-of-study

Fill up Program of Study Non-Thesis Other Scholarship
    [Arguments]    ${email}    ${1}    ${2}    ${3}    ${4}    ${5}
    ...    ${6}    ${7}    ${8}
    Login and go to Program of Study    ${email}
    Sleep    5
    Click Element    xpath=(//div[text() = '${1}'])
    Click Element    xpath=(//div[text() = '${2}'])
    Click Element    xpath=(//div[text() = '${3}'])
    Click Element    xpath=(//div[text() = '${4}'])
    Click Element    xpath=(//div[text() = '${5}'])
    Input Text    name=year    ${6}
    Click Element    xpath=(//div[text() = '${7}'])
    Input Text    name=scholarship_name    ${8}
    Click Element    id=submit
    Location Should Be    http://${HOST}/application
    ${result} =    Get Text    id=program-of-study-text
    Should Be Equal As Strings    ${result}    Answered
    Click Element    id=logout

Fill up Program of Study Thesis ERDT
    [Arguments]    ${email}    ${1}    ${2}    ${3}    ${4}    ${5}
    ...    ${6}    ${7}    ${8}    ${9}    ${10}
    Login and go to Program of Study    ${email}
    Sleep    5
    Click Element    xpath=(//div[text() = '${1}'])
    Click Element    xpath=(//div[text() = '${2}'])
    Click Element    xpath=(//div[text() = '${3}'])
    Click Element    xpath=(//div[text() = '${4}'])
    Sleep    0.5
    Click Element    xpath=(//div[text() = '1st Choice'])
    Sleep    0.5
    Click Element    xpath=(//div[text() = '${5}'])[1]
    Sleep    0.5
    Click Element    xpath=(//div[text() = '2nd Choice'])
    Sleep    0.5
    Click Element    xpath=(//div[text() = '${6}'])[2]
    Sleep    0.5
    Click Element    xpath=(//div[text() = '3rd Choice'])
    Sleep    0.5
    Click Element    xpath=(//div[text() = '${7}'])[3]
    Click Element    xpath=(//div[text() = '${8}'])
    Input Text    name=year    ${9}
    Click Element    xpath=(//div[text() = '${10}'])
    Click Element    id=submit
    Location Should Be    http://${HOST}/application
    ${result} =    Get Text    id=program-of-study-text
    Should Be Equal As Strings    ${result}    Answered
    Click Element    id=logout

Check GMail Account for confirmation E-mail
    [Arguments]    ${email}
    Setup    https://www.gmail.com/
    Input Text    identifierId    ${email}
    Click Element    identifierNext
    ${password} =    Get Value From User    Input password    hidden=yes
    Input Text    name=password    ${password}
    Click Element    passwordNext
    Wait Until Page Contains    upd.ngse.test
    Close Browser
