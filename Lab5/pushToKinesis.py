# This program sends the data to kinesis. You do not need to modify this code except the Kinesis stream name.
# Usage python pushToKinesis.py <file name>
# a lambda function will be triggered as a result, that will send it to AWS ML for classification
# Usage python pushToKinesis.py <csv file name with extension>

import sys,csv,json

import boto3
import boto
sys.path.append('../utils')

KINESIS_STREAM_NAME = 'mtastream'

ACCOUNT_ID = '780426777867'
IDENTITY_POOL_ID = 'us-east-1:7c514cf7-9351-4f33-9d84-53a6cf76bc72'
ROLE_ARN = 'arn:aws:iam::780426777867:role/Cognito_edisonDemoKinesisUnauth_Role'
cognito = boto.connect_cognito_identity()
cognito_id = cognito.get_id(ACCOUNT_ID, IDENTITY_POOL_ID)
oidc = cognito.get_open_id_token(cognito_id['IdentityId'])
sts = boto.connect_sts()
assumedRoleObject = sts.assume_role_with_web_identity(ROLE_ARN, "XX", oidc['Token'])
def main(fileName):
    global KINESIS_STREAM_NAME    
    # connect to kinesis
    kinesis = boto.connect_kinesis(
            aws_access_key_id = assumedRoleObject.credentials.access_key,
            aws_secret_access_key=assumedRoleObject.credentials.secret_key,
            security_token = assumedRoleObject.credentials.session_token)
   # kinesis = aws.getClient('kinesis','us-east-1')
    data = [] # list of dictionaries will be sent to kinesis
    with open(fileName,'rb') as f:
    	dataReader = csv.DictReader(f)
        for row in dataReader:
            print row
            kinesis.put_record(stream_name=KINESIS_STREAM_NAME, data=json.dumps(row), partition_key='TimeStamp,delta96,delta42,Day')
           # kinesis.put_records(
            #        Record = {
             #           (
              #              row
         #   kinesis.get_recordis(1)
        #    break
        
    f.close() 




if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Missing arguments"
        sys.exit(-1)
    if len(sys.argv) > 2:
        print "Extra arguments"
        sys.exit(-1)
    try:
        fileName = sys.argv[1]
        main(fileName)
    except Exception as e:
        raise e
