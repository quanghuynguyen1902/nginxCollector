import json
from bson import json_util

from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='kafka:9092')
data = [
    {"timestamp": "2021-05-13T14:04:23.350000Z", "created_at": 1618322662.35, "status": 404, "size": 0},
{"timestamp": "2021-05-13T14:04:21.319000Z", "created_at": 161832.319,  "status": 704, "size": 0}
]
for i in range(2):
    producer.send('requests', json.dumps(data[i], default=json_util.default).encode('utf-8'))
    producer.flush()