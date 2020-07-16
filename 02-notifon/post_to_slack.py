# coding: utf-8
import requests
url = '' #Replace with slack webhook
data = {"text":"Hello, It's Saima."}
requests.post(url, json=data)
