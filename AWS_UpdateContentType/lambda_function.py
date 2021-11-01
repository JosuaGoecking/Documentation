import boto3
import time, urllib.parse
import json

s3 = boto3.client('s3')

def lambda_handler(event, context):
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    object_key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
    target_bucket = '<target-bucket>'
    copy_source = {'Bucket': source_bucket, 'Key': object_key}
    try:
        # Using waiter to wait for the object to persist through s3 service
        waiter = s3.get_waiter('object_exists')
        waiter.wait(Bucket=source_bucket, Key=object_key)
        # Copy object to target bucket with adapted ContentType
        s3.copy_object(Bucket=target_bucket, Key=object_key, ContentType='binary/octet-stream', CopySource=copy_source, MetadataDirective='REPLACE')
        # Delete object from source bucket
        s3.delete_object(Bucket=source_bucket, Key=object_key)
        return response['ContentType']
    except Exception as err:
        print ("Error -"+str(err))
        return err

