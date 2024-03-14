import boto3
import pandas as pd

ENDPOINT = ''
BUCKET = ''

# Create a client
client = boto3.client(service_name='s3', endpoint_url=ENDPOINT)

# Create a reusable Paginator
paginator = client.get_paginator('list_objects_v2')

# Create a PageIterator from the Paginator
page_iterator = paginator.paginate(Bucket=BUCKET)

founded_kyes = []
for page in page_iterator:
    for item in page['Contents']:
        founded_kyes.append(item['Key'])

result_string = ''
for key in founded_kyes:
    obj = client.get_object(Bucket = BUCKET, Key=key)
    result_string += obj['Body'].read().decode('utf-8')

output_frame = pd.read_json(result_string, convert_dates=False, lines=True)