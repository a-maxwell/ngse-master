*** Settings ***
Resource          resources.robot

*** Variables ***

*** Test Cases ***
Test Registration Non-ERDT
    Open Browser    http://${HOST}    ${BROWSER}
    Wait Until Angular Ready
    Input Text    model=registration.last    Montemayor
    Input Text    model=registration.given    Gerard
    Input Text    model=registration.middlemaiden    Borja
    Input Text    model=registration.email    gbmontemayor@up.edu.ph
    Click Element    name=register

Navigate to Site
    [Documentation]    Navigate to the NGSE Website
    ...    http://localhost:6543
