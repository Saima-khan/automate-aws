# coding: utf-8
import boto3
session = boto3.Session(profile_name='pythonAutomation')
s3 = session.resource('s3')
s3.create_bucket(Bucket='skvideoanalyzer')
s3.buckets.all()
for bucket in s3.buckets.all():
    print(bucket)
    
pathname = '/home/sa.khan/Downloads/Pexels Videos 2796268.mp4'
path = Path(pathname).expanduser().resolve()
from pathlib import Path
path = Path(pathname).expanduser().resolve()
path.name
path
bucket = s3.Bucket(name='skvideoanalyzer')
bucket.upload_file(str(path),str(path.name))
rekognition_client = session.resource('rekognition')
rekognition_client = session.client('rekognition')
response = rekognition_client.start_label_detection(Video={'S3Object': {'Bucket': bucket.name, 'Name': path.name}})
response
job_id = response['JobId']
result = rekognition_client.get_label_detection(JobId=job_id)
result.keys()
result['JobStatus']
result['ResponseMetadata']
result['VideoMetadata']
result['Labels']
list(result['Labels'])
len(result['Labels'])
get_ipython().run_line_magic('label-detection.py', '1-100')
get_ipython().run_line_magic('save', 'label-detection.py 1-100')
