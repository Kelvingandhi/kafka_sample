import time
import json
from datetime import datetime
from data_generator import generate_random_data
from kafka import KafkaProducer

# Serialize messages as JSON
def serializer(message):
    return json.dumps(message).encode('utf-8')


#Kafka Producer
producer = KafkaProducer(
    bootstrap_servers = ['localhost:9092'],
    value_serializer = lambda x: json.dumps(x).encode('utf-8')
)

if __name__ == '__main__':

    #Infinite Loop to generate data continuously
    while True:

        #Generate a message
        sample_message = generate_random_data()

        #send message to Kafka Topic
        print(f'Producing message @ {datetime.now()} \nMessage: {str(sample_message)}')
        producer.send('first_topic',sample_message)
        producer.flush()
        #sleep for 5 seconds
        time.sleep(5)
        