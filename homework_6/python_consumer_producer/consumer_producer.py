from kafka import KafkaProducer, KafkaConsumer

consumer = KafkaConsumer('postgres_customer_actions', bootstrap_servers=['kafka:9092', 'kafka-r2:9092', 'kafka-r3:9092'])

for msg in consumer:
    print(msg)
