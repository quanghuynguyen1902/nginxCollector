from kafka import KafkaConsumer
consumer = KafkaConsumer('requests',  bootstrap_servers=['kafka:9092'])
for message in consumer:
    print (message)