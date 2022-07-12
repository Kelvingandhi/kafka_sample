import time
import json
from datetime import datetime
from main import fetch_city_bike_data, retrieve_city_bike_data
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

        #Fetch data from Web URL & Post it to Local API using POST request
        fetch_city_bike_data()
        time.sleep(2)

        #Retrieve data from Local API using GET request
        city_bike_data = retrieve_city_bike_data()

        #send message to Kafka Topic
        print(f'Producing message @ {datetime.now()} \nMessage: {str(city_bike_data)}')
        producer.send('city_bike_topic',city_bike_data)
        producer.flush()
        #sleep for 8 seconds
        time.sleep(8)
        