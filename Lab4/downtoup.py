import json,time,sys
import thread
from collections import OrderedDict
import threading
from threading import Thread
from botocore.exceptions import ClientError
import boto3, boto
from boto3.dynamodb.conditions import Key,Attr
from boto.dynamodb2.fields import HashKey, RangeKey
import boto.dynamodb2
sys.path.append('../utils')
import tripupdate,vehicle,alert,mtaUpdates,aws
import datetime
import boto.sns
import math

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
sns=boto.sns.connect_to_region(
        'us-east-1',
        aws_access_key_id=assumedRoleObject.credentials.access_key,
        aws_secret_access_key=assumedRoleObject.credentials.secret_key,
        security_token=assumedRoleObject.credentials.session_token)

stop={"103 St":"119N","110 St":"118N","116 St":"117N","125 St":"116N","137 St":"115N","145 St":"114N","157 St":"113N","168 St":"112N","181 St":"111N","191 St":"110N","Dyckman St":"109N","207 St":"108N","":"",}
phone_arn={}
def query_train(routeid):
    response=MTA.scan(routeId__eq=routeid)
    trainlist=[]
    for i in response:
        futurestopsdata=i.values()[5]
        if "127N" in futurestopsdata:
            trainlist.append(i.values()[8])
    return trainlist
def find_earlist(trainlist):
    earlist=100000000000000
    eid = "none"
    for i in trainlist:
        response=MTA.query_2(tripId__eq=i)
        for j in response:
            futurestopsdata=j.values()[5]
        a = futurestopsdata["127N"]#[0].get('arriveTime')
        b = a[0]
        c = b["arriveTime"]
        if earlist > int(c):
            earlist = int(c)
            eid = i
    return eid 
def timetaken(idlist):
    c=100000000000000
    time = [c,c,c]
    count = 0
    for i in idlist:
        response=MTA.query_2(tripId__eq=i)
        for j in response:
            futurestopsdata=j.values()[5]
            a = futurestopsdata["120N"]
            b = a[0]
            c = b["arriveTime"]
            time[count]=c
        count = count+1
    return time
def finaltime23(arrivetime,destination):
    response=MTA.scan(routeId__eq='1')
    mintime=100000000000000
    minid=""
    for i in response:
        futuredata = i.values()[5]
        if "120N" in futuredata:
            a=futuredata["120N"]
            b=a[0]
            c=b["arriveTime"]
            if int(c) > int(arrivetime):
                if int(mintime) > int(c):
                    mintime = int(c)
                    minid = i
    finaltime=minid.values()[5][destination][0]["arriveTime"]
                
    return finaltime

line1=query_train('1')
line2=query_train('2')
line3=query_train('3')
print 'all line1 trains: ',
print line1
print 'all line2 trains: ',
print line2
print 'all line3 trains: ',
print line3

earlist1=find_earlist(line1)
earlist2=find_earlist(line2)
earlist3=find_earlist(line3)
el=[earlist1,earlist2,earlist3]
print 'tripid of earlist 1, 2, 3 trains',
print el
arrivetime = timetaken(el)
print arrivetime
while (True):
    request=raw_input("1:Plan trip 2:Subscribe to message feed 3:Exit\n")
    if request=="1":
        phonenumber=raw_input("Please enter your phone number:\n")
        destination=raw_input("Please enter your destination:\n")
       # if destination not in stop:
        #    print "Re-enter your destination"
       # else:
        destination=stop[destination]
        response=MTA.query_2(tripId__eq=earlist1)
        for j in response:
            futurestopdata=j.values()[5]
            finaltime1=futurestopdata[destination][0]["arriveTime"]
        finaltime2=finaltime23(arrivetime[1],destination)
        finaltime3=finaltime23(arrivetime[2],destination) 
        mintime=min(int(finaltime1),int(finaltime2),int(finaltime3))
        print 'time 1:',
        print int(finaltime1)-int(time.time())
        print 'time 2:',
        print int(finaltime2)-int(time.time())
        print 'time 3:',
        print int(finaltime3)-int(time.time())
        if mintime == int(finaltime1):
            resultid=earlist1
            msg='Take the local train, and the time taken is '+str(int(finaltime1)-int(time.time()))+'s'
        if mintime == int(finaltime2):
            resultid = earlist2
            msg='Take express 2 train, and the time taken is '+str(int(finaltime2)-int(time.time()))+'s'
        if mintime == int(finaltime3):
            resultid = earlist3
            msg='Take express 3 train, and the time taken is '+str(int(finaltime3)-int(time.time()))+'s'       
        sns.publish(message=msg,target_arn=topicarn)
        
    elif request=="2":
        phonenumber=raw_input("phone number\n")
        if phonenumber in phone_arn:
            topicarn = phone_arn[phonenumber]
        else:
            topicname = phonenumber
            topicarn = sns.create_topic(topicname)
            topicarn = topicarn['CreateTopicResponse']
            topicarn = topicarn['CreateTopicResult']
            topicarn = topicarn['TopicArn']
            phone_arn[phonenumber] = topicarn
            sns.subscribe(topicarn,"sms",phonenumber)
            
    else:
        exit()
