from kafka import KafkaConsumer
consumer = KafkaConsumer('requests',  bootstrap_servers=['localhost:9092'])
for message in consumer:
    print (message)