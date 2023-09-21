#!/usr/bin/python3
import requests , pycurl, json

api_key = "P8ahPHp6GiDVgvIVSzqV2l3gFGxLAp3d"
base_url = "https://app.ticketmaster.com/discovery/v2/"
test_event="events.json"
test_url = "https://app.ticketmaster.com/discovery/v2/events.json?apikey=P8ahPHp6GiDVgvIVSzqV2l3gFGxLAp3d"
def api_call(url):
    respone = requests.get(url)
    print(respone.status_code)
    return respone.json()




##testing
a = api_call(test_url)
print(json.dumps(a, indent=1))
