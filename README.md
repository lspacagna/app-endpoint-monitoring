# AppDynamics Endpoint Monitoring

## Introduction

This Python script can be run locally or within the AppDynamics Synthetics product.
It connects to your chosen URL and times the response time and records the response code.
This information is then stored in a custom analytics schema inside AppDynamics analytics.

## Pre-requisites

1. A python3 installation and AppDynamics Synthetics.

## Running locally & setting up custom analytics schema

1. Set appropriate environment variables. Edit the values in env-var.sh to the values for the controller you'd like to send the data to.
2. Run the following command to set the environment variables

```
$ source env-var.sh
```
3. Edit the url variable at the start of the script to the URL that you would like to test.
4. Setup custom analytics schema by running the following command.

```
python3 endpoint.py createSchema <schema-name>
```

5. Run the script to perform the timed request.

```
python3 endpoint.py runTest1 <schema-name>
```

6. The results of the test will be recorded in the custom analytics schema created in step 4. 
