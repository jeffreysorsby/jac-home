import pandas as pd
import boto3

s3_client = boto3.client('s3',
    aws_access_key_id='AKIAIUASAYLUYR7MQ4OA',
    aws_secret_access_key='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')

response = s3_client.list_objects_v2(Bucket='jac.mx')
df = pd.DataFrame(response['Contents'])
