import re
from urllib import response
from faker import Faker
import random
import requests

fake = Faker()

def generate_random_data():

    id = random.randint(0, 100)
    name = fake.unique.name()
    address = fake.address()
    email = fake.email()
    phone = fake.phone_number()

    res = {'Id': id, 'Name': name, 'Address': address, 'Email': email, 'Phone': phone}

    return res

osla_headers = {
        'Client-Identifier': 'dan-citymonitor',
}
def fetch_osla_bike_data():
    #response = requests.get('https://gbfs.urbansharing.com/oslobysykkel.no/station_status.json', 
    #            headers=osla_headers)

    response = requests.get('https://gbfs.citibikenyc.com/gbfs/en/station_status.json')
    return response.json()