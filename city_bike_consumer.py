import json
from typing import Dict
from kafka import KafkaConsumer

station_status = dict()

if __name__ == '__main__':
    consumer = KafkaConsumer(
            'city_bike_topic',
            bootstrap_servers = ['localhost:9092'],
            auto_offset_reset='earliest',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    for message in consumer:
        if message is not None:
            #print(message.value)
            message = message.value
            
            station_status['last_updated'] = message['last_updated']
            
            i = 0
            for station in message['data']['stations']:

                station_status['station_id'] = station['station_id']
                station_status['num_bikes_available'] = station['num_bikes_available']
                station_status['num_docks_available'] = station['num_docks_available']

                print(station_status)

                i = i + 1
                if i == 4:
                    break
    #print(consumer.topics())