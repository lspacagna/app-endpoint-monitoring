from selenium import webdriver
import os
import sys
import requests
import datetime
import random
import json

url = "https://postman-echo.com/post"
schemaName = "syntheticEvents"

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

def runTestCase1(testURL):
    statusCode, responseTime, testedUrl = postRequest( testURL )
    data = collateData(statusCode, responseTime, testedUrl)
    postCustomAnalytics()


if "driver" not in dir(): # Execute as script from command line
    print( "Running as script")

    # Source authentication credentials from environment variables
    auth = { "endPoint":            os.environ.get('APPDYNAMICS_EVENTS_SERVICE_ENDPOINT'),
             "globalAccountName":   os.environ.get('APPDYNAMICS_GLOBAL_ACCOUNT_NAME'),
             "analyticsKey":        os.environ.get('APPDYNAMICS_ANALYTICS_API_KEY'),
             "controllerHost":      os.environ.get('APPDYNAMICS_CONTROLLER_HOST_NAME'),
             "controllerPort":      os.environ.get('APPDYNAMICS_CONTROLLER_PORT'),
             "controllerAdminUser": os.environ.get('APPD_CONTROLLER_ADMIN'),
             "controllerAccount":   os.environ.get('APPDYNAMICS_AGENT_ACCOUNT_NAME'),
             "controllerPwd":       os.environ.get('APPD_UNIVERSAL_PWD'),
             "schemaName":          "" }

    def get_measurement_id():
        return "(local)"

    runTestCase1(url)

else: # Assume running within AppDynamics Synthetic Agent Framework
    print( "Running in AppDynamics Synthetic Agent Framework")

    runTestCase1(url)
