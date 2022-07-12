import json
from kafka import KafkaConsumer

if __name__ == '__main__':
    consumer = KafkaConsumer(
            'first_topic',
            bootstrap_servers = ['localhost:9092'],
            auto_offset_reset='earliest',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    for message in consumer:
        if message is not None:
            print(message.value)

    #print(consumer.topics())