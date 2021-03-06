import math
import mraa
import pyupm_i2clcd as lcd
import pyupm_grove as grove
import time
import boto
from boto import kinesis
from boto.dynamodb2.fields import HashKey, RangeKey
import boto.dynamodb2
from time import gmtime, strftime
import pexpect
import sys

# 
def floatfromhex(h):
    t = float.fromhex(h)
    if t > float.fromhex('7FFF'):
        t = -(float.fromhex('FFFF') - t)
        pass
    return t



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

# LCD
myLcd = lcd.Jhd1313m1(0, 0x3E, 0x62)
myLcd.setColor(53, 39, 249)
myLcd.setCursor(0,0)
myLcd.write("Current Mode")

# swith
switch_pin_number=8
switch = mraa.Gpio(switch_pin_number)
switch.dir(mraa.DIR_IN)

# Kinesis
KINESIS_STREAM_NAME = 'edisonDemoKinesis'
# Prepare Kinesis client
client_kinesis = boto.connect_kinesis(
            aws_access_key_id=assumedRoleObject.credentials.access_key,
            aws_secret_access_key=assumedRoleObject.credentials.secret_key,
            security_token=assumedRoleObject.credentials.session_token)
shard_count = 1
try:
    stream = client_kinesis.create_stream(KINESIS_STREAM_NAME, shard_count)
except:
    stream = client_kinesis.describe_stream(KINESIS_STREAM_NAME)

try:
    Temperature = Table.create('Temperature', schema=[HashKey('Timestamp')], connection=client_dynamo)
    time.sleep(30)
except:
    Temperature = Table('Temperature', connection=client_dynamo)
# set mode: 1 for DynamoDB storing data, 2 for Kinesis analysing data.
mode = 1

def test(gpio):
    global mode
    time.sleep(0.5)
    print 'interrupt'
    mode = 1-mode
    print mode

switch.isr(mraa.EDGE_RISING, test, switch)

tool = pexpect.spawn('gatttool -b 00:10:18:01:38:2B --interactive')
tool.expect('\[LE\]>')
print "Preparing to connect. You might need to press the side button..."
tool.sendline('connect')
tool.expect('Connection successful')
tool.sendline('char-write-req 0x2b 0x01')
tool.expect('\[LE\]>')
while (True):
    tool.sendline('char-read-hnd 0x2a')
    tool.expect('Notification handle = 0x002a value: 34 .*')
    rval = tool.after.split()
    low = floatfromhex(rval[10])
    high = floatfromhex(rval[11])
    temp = (high * 256 + low)/10
    myLcd.setCursor(1,12)
    myLcd.write(str(temp))
    # DynamoDB
    if(mode==1):
        myLcd.setCursor(1,0)
        myLcd.write("DynamoDB...")
        timestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        print timestamp
        Temperature.put_item(data={
                'Timestamp': timestamp,
                'Temperature': str(temp),
        })
        True
        time.sleep(1)
    # Kinesis
    else:
        myLcd.setCursor(1,0)
        myLcd.write("Kinesis...")
        client_kinesis.put_record(
                stream_name=KINESIS_STREAM_NAME, 
                data=str(temp), 
                partition_key='Partitionkey')
        print temp
