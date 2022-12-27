import json
import boto3
import os
import io
import requests
'''
    Upload data from API 'https://datausa.io/api/data?drilldowns=Nation&measures=Population'
    to s3 bucket
'''

bucket_name = 'rearc-project'
file_name = 'population_data.json'
source_url = 'https://datausa.io/api/data?drilldowns=Nation&measures=Population'
data_dict = json.loads(requests.get(source_url, allow_redirects=True).text)

s3 = boto3.resource('s3', aws_access_key_id=os.getenv('aws_access_key'),
    aws_secret_access_key=os.getenv('aws_secret_key'))
obj = s3.Object(bucket_name,file_name)
obj.upload_fileobj(Fileobj = io.BytesIO(str.encode(json.dumps(data_dict))))