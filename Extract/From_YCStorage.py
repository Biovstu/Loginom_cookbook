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

for i, key in enumerate(founded_kyes):
    obj = client.get_object(Bucket = 'bv-bucket-logs', Key=key)
    tmp_frame = pd.read_json(obj['Body'].read().decode('utf-8'), convert_dates=False, lines=True)
    tmp_frame['key'] = key
    if i == 0:
        output_frame = tmp_frame
    else:
        output_frame = pd.concat([output_frame, tmp_frame], axis=0, ignore_index=True)
