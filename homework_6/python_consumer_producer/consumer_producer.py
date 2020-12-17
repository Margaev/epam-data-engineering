import json
import faker

from kafka import KafkaProducer, KafkaConsumer

fake = faker.Faker()

consumer = KafkaConsumer('postgres_customer_actions',
                         bootstrap_servers=['kafka:9092', 'kafka-r2:9092', 'kafka-r3:9092'])
producer = KafkaProducer(bootstrap_servers=['kafka:9092', 'kafka-r2:9092', 'kafka-r3:9092'])

for msg in consumer:
    json_data = json.loads(msg.value)
    # print(json.dumps(json_data, indent=4))
    payload = json_data['payload']
    if payload['type'] == '3':
        payload['address'] = fake.address()
        new_msg = bytes(json.dumps(payload), encoding='utf-8')
        producer.send('de-enriched-data', new_msg)
