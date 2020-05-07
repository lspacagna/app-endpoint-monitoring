from selenium import webdriver
import os
import sys
import requests
import datetime
import random
import json
import socket
socket.gethostbyname("")

url = "https://postman-echo.com/post"
schema = { "schema": {  "testid":           "integer",
                        "status_code":      "integer",
                        "status_code_s":    "string",
                        "response_time":    "integer",
                        "url":              "string",
                        "mesid":            "string" } }


def createHeaders(auth):
    return { "X-Events-API-AccountName": auth['globalAccountName'],
             "X-Events-API-Key": auth['analyticsKey'],
             "Content-type": "application/vnd.appd.events+json;v=2",
             "Accept": "application/vnd.appd.events+json;v=2"}



def createCustomSchema(schema, auth):
    print('Creating analytics schema: '+ auth['schemaName'])
    url = auth['analyticsUrl'] + "/events/schema/" + auth['schemaName']

    try:
        r = requests.post( url,
            data=json.dumps( schema ),
            headers=createHeaders( auth ) )
        statusCode = r.status_code
    except Exception as e:
        print( "E ", e )

    print(r.status_code, r.text)

def deleteCustomSchema( auth ):
    r = requests.delete( auth['analyticsUrl'] + "/events/schema/" + auth['schemaName'],
                         headers=createHeaders( auth ) )


def postCustomAnalytics(auth, data):
    print("POSTing to AppDynamics...")

    url = auth['analyticsUrl'] + "/events/publish/" + auth['schemaName']
    print(url)

def collateData(statusCode, responseTime, testedUrl):
    data = [ {  "status_code":      statusCode,
                "response_time":    responseTime,
                "url":              testedUrl,
                "mesid":            get_measurement_id() } ]
    return data

def postRequest(testURL):
    status_code = 0
    startTime = datetime.datetime.now()

    try:
        r = requests.post( testURL )
        statusCode = r.status_code
    except Exception as e:
        print( "E ", e )
        statusCode = 503 # 503 Service Unavailable
    responseTime = int((datetime.datetime.now() - startTime).total_seconds() * 1000)
    print( "Test URL ", testURL, statusCode, responseTime )
    return int( statusCode ), responseTime, testURL

def runTestCase1(auth, testURL):
    statusCode, responseTime, testedUrl = postRequest( testURL )
    data = collateData(statusCode, responseTime, testedUrl)
    postCustomAnalytics(auth, data)


if "driver" not in dir(): # Execute as script from command line
    print( "Running as script")

    # Source authentication credentials from environment variables
    auth = { "globalAccountName":   os.environ.get('APPDYNAMICS_GLOBAL_ACCOUNT_NAME'),
             "analyticsKey":        os.environ.get('APPDYNAMICS_ANALYTICS_API_KEY'),
             "analyticsUrl":        os.environ.get('APPDYNAMICS_ANALYTICS_URL')
             }

    def get_measurement_id():
        return "(local)"

    cmd = sys.argv[1] if len(sys.argv) > 1 else "unknown command"

    if cmd == "runTest1": # runtest1 <schema name>
        auth['schemaName'] = sys.argv[2]
        runTestCase1(auth, url)

    elif cmd == "createSchema": # createSchema <schema name>
        auth['schemaName'] = sys.argv[2]
        createCustomSchema(schema, auth)

    elif cmd == "deleteSchema": # deleteSchema <schema name>
        auth['schemaName'] = sys.argv[2]
        deleteCustomSchema(auth)



else: # Assume running within AppDynamics Synthetic Agent Framework
    print( "Running in AppDynamics Synthetic Agent Framework")

    runTestCase1(url)
