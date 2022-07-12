from ast import Index
from asyncio import sleep
import stat
import time
import json
import requests
from fastapi import FastAPI, Path

from typing import Optional, List
from pydantic import BaseModel

class Station(BaseModel):
    station_id: int
    name: str
    capacity: int
    station_type: str
    num_bikes_available: int
    num_docks_available: float
    lat: float
    lon: float

class StationStatus(BaseModel):
    last_updated: str
    stations: List[Station]

station_dict = dict()

def retrieve_city_bike_data():
    
    try:
        result = requests.get('http://localhost:8000/stations_status/', headers={'Accept': 'application/json', 'Content-Type': 'application/json'})
    except requests.exceptions.RequestException as e:
        return {}

    return result.json()


def fetch_city_bike_data():
    #response = requests.get('https://gbfs.urbansharing.com/oslobysykkel.no/station_status.json', 
    #            headers=osla_headers)

    res_status = requests.get('https://gbfs.citibikenyc.com/gbfs/en/station_status.json')
    res_info = requests.get('https://gbfs.citibikenyc.com/gbfs/en/station_information.json')

    res_station_status = res_status.json()
    res_station_info = res_info.json()

    i = 0

    station_list = []

    for (status, info) in zip(res_station_status['data']['stations'],res_station_info['data']['stations']):
        
        record = Station(station_id=status['station_id'], name=info['name'], capacity=info['capacity'],
                station_type=info['station_type'], num_bikes_available=status['num_bikes_available'], 
                num_docks_available=status['num_docks_available'], lat=info['lat'], lon=info['lon'])
        station_list.append(record)

        i += 1

        if i == 5:
            break

    station_status = StationStatus(last_updated=res_station_status['last_updated'], stations=station_list)

    my_response = requests.post('http://localhost:8000/stations/', data=station_status.json(), headers={"accept": "application/json","Content-type": "application/json"})

    #return station_status.json()
    return

app = FastAPI()

final = {}

@app.get('/stations_status')
async def getStationInfo():
    return station_dict

@app.get('/stations/{station_id}')
async def getStationInfo(station_id:int):
    try:
        final = dict(list(filter(lambda x: x.station_id == station_id, station_dict['stations']))[0])
        return final
    except IndexError:
        return {station_id : "station does not exist"}

@app.post('/stations')
async def postStationInfo(station_status:StationStatus):
    station_dict['last_updated'] = station_status.last_updated
    station_dict['stations'] = station_status.stations
    return station_status

def kick_off_API():
    while True:
        res = fetch_city_bike_data()
        
        print(res)

        time.sleep(8)

if __name__ == '__main__':

    while True:
        kick_off_API()
        # print(fetch_city_bike_data())
        # time.sleep(5)
        # print(retrieve_city_bike_data())

