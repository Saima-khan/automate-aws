# coding: utf-8
event = {'Records': [{'eventVersion': '2.1', 'eventSource': 'aws:s3', 'awsRegion': 'us-east-1', 'eventTime': '2020-07-17T09:57:21.957Z', 'eventName': 'ObjectCreated:Put', 'userIdentity': {'principalId': 'AWS:AIDAVRGATPFLI3ZZKEICP'}, 'requestParameters': {'sourceIPAddress': '180.151.247.147'}, 'responseElements': {'x-amz-request-id': '4QCN1K6Q7K5MEZCG', 'x-amz-id-2': 'K0mPCTOLn4OqPOBDoQliioHn1L/6JH3zwTIID7Zq5LiGWCreWyR42KACAgSxx01yo2vGAOt8cpi+GxuIUw1M1LsYXvoPYp3u'}, 's3': {'s3SchemaVersion': '1.0', 'configurationId': 'a9c2e0ca-3867-48af-9630-83249c5b8c47', 'bucket': {'name': 'skvideoanalyzer123', 'ownerIdentity': {'principalId': 'AB1FEFEUTBZ8C'}, 'arn': 'arn:aws:s3:::skvideoanalyzer123'}, 'object': {'key': 'Pexels+Videos+1234163.mp4', 'size': 3227305, 'eTag': 'c7c0ed5ae09edc4bce1646c638b335d2', 'sequencer': '005F1175E3C1DDF30B'}}}]}
event
event['Record'][0]['s3']['bucket']['name']
event['Records'][0]['s3']['bucket']['name']
event['Records'][0]['s3']['bucket']['key']
event['Records'][0]['s3']['object']['key']
event['Records'][0]['s3']['object']['key']
import urllib
urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
