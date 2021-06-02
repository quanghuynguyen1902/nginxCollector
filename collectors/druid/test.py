import requests

# api push data to druid
druidURL = 'http://coordinator:8081/druid/indexer/v1/supervisor'
druid_schema_path = "kafka.json"
headers =  {'content-type': 'application/json'}
with open(druid_schema_path, 'rb') as f:
    response = requests.post(druidURL, headers=headers, data=f).json()
    print(response)