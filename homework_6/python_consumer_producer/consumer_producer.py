import json
import faker

from kafka import KafkaProducer, KafkaConsumer

fake = faker.Faker()

consumer = KafkaConsumer('de-source-data',
                         bootstrap_servers=['kafka-1:9092', 'kafka-2:9092', 'kafka-3:9092'])
producer = KafkaProducer(bootstrap_servers=['kafka-1:9092', 'kafka-2:9092', 'kafka-3:9092'])

for msg in consumer:
    json_data = json.loads(msg.value)
    data = json_data['payload']['after']

    if data['type'] == '3':
        data['address'] = fake.address()
        new_msg = bytes(json.dumps(data), encoding='utf-8')
        partition = int(data['customer_id'])
        producer.send('de-enriched-data', new_msg, partition=partition)
