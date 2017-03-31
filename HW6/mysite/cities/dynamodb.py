import json,time,sys
import thread
from threading import Thread
from botocore.exceptions import ClientError
import boto
from boto.dynamodb2.fields import HashKey, RangeKey
import boto.dynamodb2
from weatherAPI import temlist, citylist
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
DYNAMODB_TABLE_NAME = 'cityweather'

# DynamoDB
client_dynamo = boto.dynamodb2.connect_to_region(
        'us-east-1',
        aws_access_key_id=assumedRoleObject.credentials.access_key,
        aws_secret_access_key=assumedRoleObject.credentials.secret_key,
        security_token=assumedRoleObject.credentials.session_token)
from boto.dynamodb2.table import Table
table_dynamo = Table(DYNAMODB_TABLE_NAME, connection=client_dynamo)
try:
    cityweather = Table.create('cityweather', schema=[HashKey('name')], connection=client_dynamo)
    time.sleep(30)
except:
    cityweather = Table('cityweather', connection=client_dynamo)

### YOUR CODE HERE ####
def adding():
    while(True):
        start=time.time()
        print 'adding data...'
        
        for i in range(0,len(temlist)):
            
            cityweather.put_item(data={
                'name' : citylist[i],
                'temp_max' : str(temlist[citylist[i]]['temp_max']),
                'temp_kf' : str(temlist[citylist[i]]['temp_kf']),
                'temp': str(temlist[citylist[i]]['temp']),
                'temp_min':str(temlist[citylist[i]]['temp_min']),
                },overwrite=True)
                
        end = time.time()
        time.sleep(30-(end-start))


# define two threads
adding()
