#!/usr/bin/python3
import requests , pycurl


url = 'https://www.eventbriteapi.com/v3/users/me/?token=4B2WKIGMY7VW2T356IXQ'


def curl_request():
    # Create a Curl object
    curl = pycurl.Curl()

    # Set the URL
    url = "https://www.eventbriteapi.com/v3/organizations/4B2WKIGMY7VW2T356IXQ/events/"
    curl.setopt(pycurl.URL, url)
   
    # Set the HTTP method to GET
    curl.setopt(pycurl.HTTPGET, 1)

    # Set request headers
    headers = [
        "Authorization: Bearer 4B2WKIGMY7VW2T356IXQ",
    ]
    curl.setopt(pycurl.HTTPHEADER, headers)

    # Perform the HTTP request
    curl.perform()

    # Get the response code
    response_code = curl.getinfo(pycurl.RESPONSE_CODE)
    print("Response Code:", response_code)

    # Get the response body
    response_body = curl.getinfo(pycurl.RESPONSE_BODY)
    print("Response Body:", response_body)

    # Clean up
    curl.close()
    



## for now api_call function tested and it work. 
def api_call(url):
    respone = requests.get(url)
    print(respone.status_code)
    return respone.json()

a = api_call(url)
print(a)