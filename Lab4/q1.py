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
#import collection

phone_arn = OrderedDict()




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
def query_train(routeid):
    response=MTA.scan(routeId__eq=routeid)
    trainlist=[]
    for i in response:
        futurestopsdata=i.values()[5]
        if "120S" in futurestopsdata:
           # print i.values()[8]
            trainlist.append(i.values()[8])
    return trainlist
def query_train1(routeid):
    response=MTA.scan(routeId__eq=routeid)
    trainlist=[]
    for i in response:
        futurestopsdata=i.values()[5]
        if "117S" in futurestopsdata:
           # print i.values()[8]
            trainlist.append(i.values()[8])
    return trainlist
def find_earlist(trainlist):
    earlist=100000000000000
    eid = "none"
    for i in trainlist:
        response=MTA.query_2(tripId__eq=i)
        for j in response:
            futurestopsdata=j.values()[5]
        a = futurestopsdata["120S"]#[0].get('arriveTime')
        b = a[0]
        c = b["arriveTime"]
        if earlist > int(c):
            earlist = int(c)
            eid = i
    
    return eid 
def timetaken(idlist):
    mintime = 100000000000000
    minid = '' 
    for i in idlist:
        response=MTA.query_2(tripId__eq=i)
        for j in response:
            futurestopsdata=j.values()[5]
            a = futurestopsdata["127S"]
            b = a[0]
            c = b["arriveTime"]
            print c
            if mintime > int(c):
                mintime = int(c)
                minid = i
    return minid, mintime

def finaltime23(arrivetime, line):
    destination = '127S'
    
    response = MTA.scan(routeId__eq=line)
    mintime = 100000000000000
    minid = ""
    for i in response:
        futuredata = i.values()[5]
        if '120S' in futuredata:
            a = futuredata['120S']
            b = a[0]
            c = b['arriveTime']
            if int(c) > int(arrivetime):
                if int(mintime)> int(c):
                    mintime = int(c)
                    minid = i
    finaltime = minid.values()[5][destination][0]['arriveTime']
    return finaltime
#target_arn='arn:aws:sns:us-east-1:780426777867:mta_topic'
while (True):
    line116 = query_train1('1')   #id
    earlist116 = find_earlist(line116)   #id
    response = MTA.query_2(tripId__eq=earlist116)
    for i in response:
        futurestopsdata=i.values()[5]
        a = futurestopsdata['117S']
        b = a[0]
        c = b["arriveTime"]
        t116to96 = c   
    time2 = finaltime23(t116to96, '2')
    time3 = finaltime23(t116to96, '3')

    response = MTA.query_2(tripId__eq=earlist116)
    for i in response:
        futurestopsdata=i.values()[5]
        a = futurestopsdata['127S']
        b = a[0]
        c = b["arriveTime"]
        t116to42 = c
    time1 = t116to42
    time1 = int(time1)-int(time.time())
    time2 = int(time2)-int(time.time())
    time3 = int(time3)-int(time.time())
    print 'time of line1: ',
    print time1
    print 'time of line2: ',
    print time2
    print 'time of line3: ',
    print time3
    earlistrouteid='0'
    kkk=min(time1,time2,time3)
    if kkk==time1:
        earlistrouteid = '1'
    elif kkk==time2:
        earlistrouteid = '2'
    else:
        earlistrouteid = '3'
    
    request=raw_input("1:Plan trip 2:Subscribe to message feed 3:Exit\n")
    if request=="1":
        phonenumber = raw_input("Please enter your phonenumber\n")
        topicarn = phone_arn[phonenumber]
        line1=query_train('1')
        print 'trains on line1:',
        print line1
        earlist1=find_earlist(line1)
        print 'earlist line1 train id:',
        print earlist1
        line2=query_train('2')
        print 'trains on line2:',
        print line2
        earlist2=find_earlist(line2)
        print 'earlist line2 train id:',
        print earlist2
        line3=query_train('3')
        print 'trains on line3:',
        print line3
        earlist3=find_earlist(line3)
        print 'earlist line3 train id:',
        print earlist3
        #idlist=[earlist1,earlist2,earlist3]
        #earlistcase,earlisttime=timetaken(idlist)
        #earlistrouteid=str(earlistcase)[str(earlistcase).index('_')+1]
        if earlistrouteid=='1':
            s='Stay on in the Local Train, time: '+str(time1)
            sns.publish(message=s,target_arn=topicarn)
        elif earlistrouteid=='2':
            s='Switch to Express Train 2, time: '+str(time2)
            sns.publish(message=s,target_arn=topicarn)
        else:
            s='Switch to Express Train 3, time: '+str(time3)
            sns.publish(message=s,target_arn=topicarn)
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
