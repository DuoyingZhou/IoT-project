# *********************************************************************************************
# Program to update dynamodb with latest data from mta feed. It also cleans up stale entried from db
# Usage python dynamodata.py
# *********************************************************************************************
import json,time,sys
import thread
from collections import OrderedDict
import threading
from threading import Thread
from botocore.exceptions import ClientError
import boto3, boto
#from boto3.dynamodb.conditions import Key,Attr
from boto.dynamodb2.fields import HashKey, RangeKey
import boto.dynamodb2
sys.path.append('../utils')
import tripupdate,vehicle,alert,mtaUpdates,aws
import datetime
# AWS ID
ACCOUNT_ID = '780426777867'
IDENTITY_POOL_ID = 'us-east-1:7c514cf7-9351-4f33-9d84-53a6cf76bc72'
ROLE_ARN = 'arn:aws:iam::780426777867:role/Cognito_edisonDemoKinesisUnauth_Role'

# Use cognito to get an identity.
cognito = boto.connect_cognito_identity()
cognito_id = cognito.get_id(ACCOUNT_ID, IDENTITY_POOL_ID)
oidc = cognito.get_open_id_token(cognito_id['IdentityId'])

# Further setup your STS using the code below
sts = boto.connect_sts()
assumedRoleObject = sts.assume_role_with_web_identity(ROLE_ARN, "XX", oidc['Token'])

# table
DYNAMODB_TABLE_NAME = 'MTA'

# DynamoDB
client_dynamo = boto.dynamodb2.connect_to_region(
        'us-east-1',
        aws_access_key_id=assumedRoleObject.credentials.access_key,
        aws_secret_access_key=assumedRoleObject.credentials.secret_key,
        security_token=assumedRoleObject.credentials.session_token)
from boto.dynamodb2.table import Table
table_dynamo = Table(DYNAMODB_TABLE_NAME, connection=client_dynamo)
try:
    MTA = Table.create('MTA', schema=[HashKey('tripId')], connection=client_dynamo)
    time.sleep(30)
except:
    MTA = Table('MTA', connection=client_dynamo)

### YOUR CODE HERE ####
def adding():
    while(True):
        start=time.time()
        print 'adding data...'
        updates = mtaUpdates.mtaUpdates()
        tripupdates, alerts = updates.getTripUpdates()
        time.sleep(2)
        for i in range(0,len(tripupdates)):
            MTA.delete_item(tripId=str(tripupdates[i].tripId))
            MTA.put_item(data={
                'timestamp' : (int)(time.time()),
                'tripId' : str(tripupdates[i].tripId),
                'routeId' : str(tripupdates[i].routeId),
                'startDate' : str(tripupdates[i].startDate),
                'direction' : str(tripupdates[i].direction),
                'currentStopId' : str(tripupdates[i].vehicleData.currentStopId),
                'currentStopStatus' : str(tripupdates[i].vehicleData.currentStopStatus),
                'vehicleTimeStamp' : str(tripupdates[i].vehicleData.timestamp),
                'futureStopData' : str(tripupdates[i].futureStops),
            })
        end = time.time()
        time.sleep(30-(end-start))

def deleting():
    response=MTA.scan()
    for i in response:
        trainkey=i.values()[3]
        response = MTA.delete_item(tripId=trainkey)
    #try:
    while(True):
        print 'deleting data...'
        start = time.time()
        twominago = int(start-120)
        #print twominago
        response=MTA.scan(timestamp__between=(1487484400,twominago))
        for i in response:
            trainkey=i.values()[3]
            MTA.delete_item(tripId=trainkey)
        end = time.time()
        time.sleep(60-(end-start))

# define two threads
t = threading.Thread(target=adding)
t.setDaemon(True)
s = threading.Thread(target=deleting)
s.setDaemon(True)
s.start()
time.sleep(10)
t.start()
time.sleep(200)
print 'ending daemon...'
