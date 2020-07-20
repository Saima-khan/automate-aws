# coding: utf-8
event = {'Records': [{'EventSource': 'aws:sns', 'EventVersion': '1.0', 'EventSubscriptionArn': 'arn:aws:sns:us-east-1:380508535126:handleLabelDetectionTopic:d4ebce9d-eece-4f77-a74b-0fd0258c9c94', 'Sns': {'Type': 'Notification', 'MessageId': 'a7c1cde5-2545-56dd-a89f-9a6a4a2c2519', 'TopicArn': 'arn:aws:sns:us-east-1:380508535126:handleLabelDetectionTopic', 'Subject': None, 'Message': '{"JobId":"b1eb05fa863dbdb773097c4f577d345d20af5c1e3ad3b0e6e0d5fb14eb991ff2","Status":"SUCCEEDED","API":"StartLabelDetection","Timestamp":1595239720897,"Video":{"S3ObjectName":"Pexels Videos 1234163.mp4","S3Bucket":"skvideoanalyzer123"}}', 'Timestamp': '2020-07-20T10:08:41.153Z', 'SignatureVersion': '1', 'Signature': 'GBEtAHYZN2tzd75Q1o9aK4oPngKb/7sD4O6s5sb9nbUKFgm/muh2rGWW0piPqLZcUJhXblVW1MGbCu88XrH4y4yN4J9ZSB/ygOn+jaER/27nE0KLsJb8dFYnjScgXwb0rPBs8Bua7hFPIxE108HJFj1DCFexm7acvUqR7kkTPm/ss8TkMjrZIXxBK0YidIssdUVCyrhqjA7/0gZVL0Qj7m1UEoCivx/Ns6GqJszyLovgDewM8JxXYxKG2qxq9TJHuRPq04/hQBwoVvd4vIfQMO+2fTEoQWkA2MV59mR4MJZQpoXAE5Gkf8xw4LqyrGCJmAwVE0UcMJF0oSJ7HNbCEQ==', 'SigningCertUrl': 'https://sns.us-east-1.amazonaws.com/SimpleNotificationService-a86cb10b4e1f29c941702d737128f7b6.pem', 'UnsubscribeUrl': 'https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-1:380508535126:handleLabelDetectionTopic:d4ebce9d-eece-4f77-a74b-0fd0258c9c94', 'MessageAttributes': {}}}]}
event['Records']
event['Records'][0]
event['Records'][0]['Sns']
event['Records'][0]['Sns']['Message']
type(event['Records'][0]['Sns']['Message'])
import json
json.loads(event['Records'][0]['Sns']['Message'])
