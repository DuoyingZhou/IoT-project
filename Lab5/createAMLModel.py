# Creating aws machine learning model
# This program uploads the finalData.csv file to S3, and used it as a data source to train a binary
# classification model
import time,sys,random

from botocore.exceptions import ClientError
import boto3
import boto
import s3

sys.path.append('../utils')
import aws

TIMESTAMP  =  time.strftime('%Y-%m-%d-%H-%M-%S')
S3_BUCKET_NAME = "abc-12345667"
S3_FILE_NAME = 'trainingdata'
S3_URI = "s3://{0}/{1}".format(S3_BUCKET_NAME, S3_FILE_NAME)
DATA_SCHEMA = "aml.csv.schema"

ACCOUNT_ID = '780426777867'
IDENTITY_POOL_ID = ***
ROLE_ARN = ***


cognito = boto.connect_cognito_identity()
cognito_id = cognito.get_id(ACCOUNT_ID, IDENTITY_POOL_ID)
oidc = cognito.get_open_id_token(cognito_id['IdentityId'])
sts = boto.connect_sts()
assumedRoleObject = sts.assume_role_with_web_identity(ROLE_ARN, "XX", oidc['Token'])

client = boto3.client('machinelearning',
        'us-east-1',
        aws_access_key_id=assumedRoleObject.credentials.access_key,
        aws_secret_access_key=assumedRoleObject.credentials.secret_key,
        aws_session_token=assumedRoleObject.credentials.session_token)




# no split
response = client.create_data_source_from_s3(
        DataSourceId='datasource_1',
        DataSourceName='trainingdata_1',
        DataSpec={
            'DataLocationS3': S3_URI,
            #'DataRearrangement': '{"splitting": {"percentBegin": 70,"percentEnd": 100}}',
            'DataSchema':'{"version" : "1.0","targetAttributeName" : "Var5","dataFormat" : "CSV","dataFileContainsHeader" : false,"attributes" : [ {"attributeName" : "Var1","attributeType" : "NUMERIC"}, {"attributeName" : "Var2","attributeType" : "NUMERIC"}, {"attributeName" : "Var3","attributeType" : "NUMERIC"}, {"attributeName" : "Var4","attributeType" : "NUMERIC"}, {"attributeName" : "Var5","attributeType" : "BINARY"} ]}'
        },
        ComputeStatistics=True,
)

# split data -- trainingdata
response = client.create_data_source_from_s3(
        DataSourceId='datasource_70_1',
        DataSourceName='trainingdata_70_1',
        DataSpec={
            'DataLocationS3': S3_URI,
            'DataRearrangement': '{"splitting": {"percentBegin": 0,"percentEnd": 70}}',
            'DataSchema':'{"version" : "1.0","targetAttributeName" : "Var5","dataFormat" : "CSV","dataFileContainsHeader" : false,"attributes" : [ {"attributeName" : "Var1","attributeType" : "NUMERIC"}, {"attributeName" : "Var2","attributeType" : "NUMERIC"}, {"attributeName" : "Var3","attributeType" : "NUMERIC"}, {"attributeName" : "Var4","attributeType" : "NUMERIC"}, {"attributeName" : "Var5","attributeType" : "BINARY"} ]}'
        },
        ComputeStatistics=True,
)

# split data -- testingdata
response = client.create_data_source_from_s3(
        DataSourceId='datasource_30_1',
        DataSourceName='trainingdata_30_1',
        DataSpec={
            'DataLocationS3': S3_URI,
            'DataRearrangement': '{"splitting": {"percentBegin": 70,"percentEnd": 100}}',
            'DataSchema':'{"version" : "1.0","targetAttributeName" : "Var5","dataFormat" : "CSV","dataFileContainsHeader" : false,"attributes" : [ {"attributeName" : "Var1","attributeType" : "NUMERIC"}, {"attributeName" : "Var2","attributeType" : "NUMERIC"}, {"attributeName" : "Var3","attributeType" : "NUMERIC"}, {"attributeName" : "Var4","attributeType" : "NUMERIC"}, {"attributeName" : "Var5","attributeType" : "BINARY"} ]}'
        },
        ComputeStatistics=True,
)

response = client.create_ml_model(
        MLModelId='mlmodel_1',
        MLModelName='mlmodel_1',
        MLModelType='BINARY',
       # Parameters={
        #        'string': 'string'
       # },
        TrainingDataSourceId='datasource_70_1',
        #Recipe='string',
        #RecipeUri='string'
)

response = client.create_evaluation(
        EvaluationId='evaluation_1',
        EvaluationName='evaluation_1',
        MLModelId='mlmodel_1',
        EvaluationDataSourceId='datasource_30_1'
)
