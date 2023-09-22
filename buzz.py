#!/usr/bin/python3
import requests , pycurl, json

api_key = "P8ahPHp6GiDVgvIVSzqV2l3gFGxLAp3d"
base_url = "https://app.ticketmaster.com/discovery/v2"
endpoint="/events.json"
city='Boston'


url = f"{base_url}{endpoint}?apikey={api_key}&countryCode=US&city={city}"



#call api
def api_call(url):
    respone = requests.get(url)
    print(respone.status_code)
    data = respone.json()
    events = data.get("_embedded", {}).get("events", [])
    return events



# "https://app.ticketmaster.com/discovery/v2/events.json?apikey=P8ahPHp6GiDVgvIVSzqV2l3gFGxLAp3d&countryCode=US&city=Boston"
# testing
events_list = api_call(url)
index = 0  
while index < len(events_list):
    event = events_list[index]
    print(f"Event Name: {event['name']}")
    print(f"Event id: {event['id']}")
    print(f"Event URL: {event['url']}")
    print("-----------------------")
    index += 1 