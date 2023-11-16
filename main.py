#!/usr/bin/python3
import requests, json, sqlite3

api_key = "P8ahPHp6GiDVgvIVSzqV2l3gFGxLAp3d"
base_url = "https://app.ticketmaster.com/discovery/v2/events"
endpoint=".json"
city='Boston'

test_event_id ="vvG17Z9cLmB6uY"

url = f"{base_url}{endpoint}?apikey={api_key}&countryCode=US&city={city}"



#call api
def api_call(url):
    respone = requests.get(url)
    #print(respone.status_code)
    data = respone.json()
    events = data.get("_embedded", {}).get("events", [])
    return events

def process_events(events):
    processed_events = []
    for event in events:
        # get id and name
        event_id = event.get('id')
        event_name = event.get('name')
        
        # get ticket range
        price_ranges = event.get('priceRanges', [])
        ticket_range = None
        if price_ranges:
            ticket_range = f"${price_ranges[0].get('min', 'N/A')} - ${price_ranges[0].get('max', 'N/A')}"

        # get date
        dates = event.get('dates', {})
        start_date = dates.get('start', {}).get('localDate', 'N/A')

        # get images
        """images = event.get('images', [])
        image_urls = [image.get('url') for image in images]"""
        images = event.get('images', [])
        image_urls = None
        for image in images:
            if image.get('ratio') == '4_3':
                image_urls = image.get('url')
                break


        # get event URL
        event_url = event.get('url')

        # get genre name
        genre_name = None
        classifications = event.get('classifications', [])
        for classification in classifications:
            if classification.get('primary'):
                genre_name = classification['genre']['name']
                break

        # Creating a dictionary with the extracted information
        processed_event = {
            'event_id': event_id,
            'event_name': event_name,
            'ticket_range': ticket_range,
            'date': start_date,
            'image_urls': image_urls,  
            'event_url': event_url,   
            'genre_name': genre_name,
        }

        # Appending the dictionary to the list
        processed_events.append(processed_event)

    return processed_events


# create database 
def create_database():
    connection = sqlite3.connect('events.db')
    cursor = connection.cursor()
    #create table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS processed_events (
            event_id TEXT PRIMARY KEY,
            event_name TEXT,
            ticket_range TEXT,
            date TEXT,
            image_urls TEXT,
            event_url TEXT,
            genre_name TEXT
            
        )
    ''')
    
    connection.commit()
    connection.close()




def update_database(processed_events):
    connection = sqlite3.connect('events.db')
    cursor = connection.cursor()

    for event in processed_events:
        cursor.execute('''
            INSERT OR REPLACE INTO processed_events (event_id, event_name, ticket_range, date, image_urls, event_url, genre_name)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (event['event_id'], event['event_name'], event['ticket_range'], event['date'],json.dumps(event['image_urls']), event['event_url'],event['genre_name']))

    connection.commit()
    connection.close()


#=====================================================================================
# "https://app.ticketmaster.com/discovery/v2/events.json?apikey=P8ahPHp6GiDVgvIVSzqV2l3gFGxLAp3d&countryCode=US&city=Boston"
# testing
events_list = api_call(url)
A = process_events(events_list)
create_database()
update_database(A)

#test function for sql table
def print_table():
    connection = sqlite3.connect('events.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM processed_events')
    rows = cursor.fetchall()

    if not rows:
        print("No records found in the table.")
    else:
        for row in rows:
            print(row)

    connection.close()

print_table()