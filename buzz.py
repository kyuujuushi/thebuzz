#!/usr/bin/python3
import requests


url = 'https://www.eventbriteapi.com/v3/users/me/?token=4B2WKIGMY7VW2T356IXQ'

##function for intergrate pyscript with website (KIR)
#def pyscript_integration():





## for now api_call function tested and it work. 
def api_call(url):
    respone = requests.get(url)
    print(respone.status_code)
    return respone.json()

a =api_call(url)
print(a)