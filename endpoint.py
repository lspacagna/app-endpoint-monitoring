from selenium import webdriver
import os
import sys
import requests
import datetime
import random
import json

url = "https://postman-echo.com/post"
schemaName = "syntheticEvents"

def createHeaders(auth):
    return { "X-Events-API-AccountName": auth['globalAccountName'],
             "X-Events-API-Key": auth['analyticsKey'],
             "Content-type": "application/vnd.appd.events+json;v=2",
             "Accept": "application/vnd.appd.events+json;v=2"}

def  postCustomAnalytics(auth, data):
    print("POSTing to AppDynamics...")

    url = auth['analyticsUrl'] + "/events/publish/" + auth['schemaName']




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
             "analyticsUrl":        os.environ.get('APPDYNAMICS_ANALYTICS_URL'),
             "schemaName":          "" }

    def get_measurement_id():
        return "(local)"

    runTestCase1(auth, url)

else: # Assume running within AppDynamics Synthetic Agent Framework
    print( "Running in AppDynamics Synthetic Agent Framework")

    runTestCase1(url)
