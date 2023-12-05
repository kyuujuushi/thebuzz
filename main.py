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




# update database
def update_database(processed_events):
    connection = sqlite3.connect('events.db')
    cursor = connection.cursor()

    for event in processed_events:
        cursor.execute('''
            INSERT OR REPLACE INTO processed_events (event_id, event_name, ticket_range, date, image_urls, event_url, genre_name)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (event['event_id'], event['event_name'], event['ticket_range'], event['date'], json.dumps(event['image_urls']), event['event_url'], event['genre_name']))

    connection.commit()
    connection.close()

# fetch new data, update database, and remove old data
def update_data():
    events_list = api_call(url)
    new_processed_events = process_events(events_list)

    # Load existing data from the database
    connection = sqlite3.connect('events.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM processed_events')
    old_processed_events = cursor.fetchall()
    connection.close()

    # Extract event_ids for comparison
    new_event_ids = set(event['event_id'] for event in new_processed_events)
    old_event_ids = set(event[0] for event in old_processed_events)

    # Calculate new, update, and delete events
    to_add = [event for event in new_processed_events if event['event_id'] not in old_event_ids]
    to_update = [event for event in new_processed_events if event['event_id'] in old_event_ids]
    to_delete = [event[0] for event in old_event_ids if event not in new_event_ids]


    # Update the database
    connection = sqlite3.connect('events.db')
    cursor = connection.cursor()
    for event in to_add:
        cursor.execute('''
            INSERT INTO processed_events (event_id, event_name, ticket_range, date, image_urls, event_url, genre_name)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (event['event_id'], event['event_name'], event['ticket_range'], event['date'], json.dumps(event['image_urls']), event['event_url'], event['genre_name']))

    for event in to_update:
        cursor.execute('''
            UPDATE processed_events
            SET event_name=?, ticket_range=?, date=?, image_urls=?, event_url=?, genre_name=?
            WHERE event_id=?
        ''', (event['event_name'], event['ticket_range'], event['date'], json.dumps(event['image_urls']), event['event_url'], event['genre_name'], event['event_id']))

    for event_id in to_delete:
        cursor.execute('DELETE FROM processed_events WHERE event_id=?', (event_id,))


    connection.commit()
    connection.close()


if __name__ == '__main__':
    EVENTS = api_call(url)
    PROCESS_EVENTS = process_events(EVENTS)
    update_database(PROCESS_EVENTS)
    update_data()
