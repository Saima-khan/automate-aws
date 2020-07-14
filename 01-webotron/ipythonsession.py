# coding: utf-8
#creates a session and s3 resource connectivity
import boto3
session = boto3.Session(profile_name = 'pythonAutomation')
s3 = session.resource('s3')
