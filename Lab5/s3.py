import boto
import boto.s3
import sys
from boto.s3.key import Key

AWS_ACCESS_KEY_ID = 'AKIAJ2T4IUNJP5STOOXQ'
AWS_SECRET_ACCESS_KEY = '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'

bucket_name = 'abc-12345667'
conn = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)

bucket = conn.create_bucket(bucket_name,
    location=boto.s3.connection.Location.DEFAULT)

testfile = "Train.csv"
print 'Uploading %s to Amazon S3 bucket %s' % \
   (testfile, bucket_name)

#def percent_cb(complete, total):
#    sys.stdout.write('.')
#    sys.stdout.flush()

k = Key(bucket)
k.key = 'trainingdata'
k.set_contents_from_filename(testfile)
