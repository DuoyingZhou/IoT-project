import time
import boto
from boto.dynamodb2.fields import HashKey, RangeKey
import boto.dynamodb2
ACCOUNT_ID = '537027909981'
IDENTITY_POOL_ID = 'us-east-1:d1dd0e2b-3dd3-4150-b7f9-a1b528151128'
ROLE_ARN = 'arn:aws:iam::537027909981:role/Cognito_edisonDemoKinesisUnauth_Role'

# Use cognito to get an identity.
cognito = boto.connect_cognito_identity()
cognito_id = cognito.get_id(ACCOUNT_ID, IDENTITY_POOL_ID)
oidc = cognito.get_open_id_token(cognito_id['IdentityId'])
 
# Further setup your STS using the code below
sts = boto.connect_sts()
assumedRoleObject = sts.assume_role_with_web_identity(ROLE_ARN, "XX", oidc['Token'])

DYNAMODB_TABLE_NAME = 'edisonDemoDynamo'

# DynamoDB
client_dynamo = boto.dynamodb2.connect_to_region(
            'us-east-1',
            aws_access_key_id=assumedRoleObject.credentials.access_key,
            aws_secret_access_key=assumedRoleObject.credentials.secret_key,
            security_token=assumedRoleObject.credentials.session_token)

from boto.dynamodb2.table import Table
table_dynamo = Table(DYNAMODB_TABLE_NAME, connection=client_dynamo)

try:
    #print '!!!!!!!!!!!!!!!!!!!'
    Columbia = Table.create('Columbia', schema=[HashKey('CUID')], connection=client_dynamo)
    time.sleep(30)
except:
    Columbia = Table('Columbia', connection=client_dynamo)

def DECISION():
    print '1:insert  2:delete  3:search  4:list all  5:quit'
    decision = raw_input('Enter your command: ')
    if decision=='1':
        cuid = raw_input('Enter your CUID: ')
        first = raw_input('Enter your first name: ')
        last = raw_input('Enter your last name: ')
        Columbia.put_item(data={
            'CUID': cuid,
            'last_name': last,
            'first_name': first,
        })
        True
        DECISION()
    elif decision=='2':
        cuid = raw_input('Enter the CUID you want to delete: ')
        Columbia.delete_item(CUID=cuid)
        DECISION()
    elif decision=='3':
        cuid = raw_input('Enter the CUID you want to search: ')
        result = Columbia.query_2(
            CUID__eq = cuid
        )
        for i in result:
            print i.values()
        DECISION()
    elif decision=='4':
        information = Columbia.scan()
        for i in information:
            print i.values()
        #print information
        DECISION()
    elif decision=='5':
        print 'Successfully exit :)'
    else:
        print "invalid input! Please try again!"
        DECISION()
    
DECISION()

# Kinesis
KINESIS_STREAM_NAME = 'edisonDemoKinesis'
# Prepare Kinesis client
client_kinesis = boto.connect_kinesis(
            aws_access_key_id=assumedRoleObject.credentials.access_key,
            aws_secret_access_key=assumedRoleObject.credentials.secret_key,
            security_token=assumedRoleObject.credentials.session_token)

