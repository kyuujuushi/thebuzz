import sqlite3
from flask import *
from icalendar import Calendar, Event
from datetime import datetime
from pathlib import Path
# - Augustus
#from flask_sqlalchemy import 
# - Augustus
import os
import pytz

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('events.db')
    conn.row_factory = sqlite3.Row
    return conn

def mk_cal (name, date):
    dateInt = []
    #nameRedo = name.replace(' ', '_')
    #trueName = nameRedo.replace('.', '')
    dateList = date.split("-")
    for i in range(len(dateList)):
        dateItem = int(dateList[i])
        dateInt.append(dateItem)

    # init the calendar
    cal = Calendar()

    #making of the event and putting it into the calendar object
    event = Event()
    event.add('name', name)
    #date is currently a dummy date will need to figure out later
    event.add('dtstart', datetime(dateInt[0], dateInt[1], dateInt[2]).date())
    cal.add_component(event)
    
    # making of the calendar file
    filename = os.path.join("./calendars", name + ".ics")
    if os.path.exists(filename) == False:
        f = open(filename, "wb")
        f.write(cal.to_ical())
        f.close()


#WIP paginated (old) - Augustus
"""

    page =
request.args.get ('page', 1,
type=int)

"""

@app.route('/about')

def about():
    return render_template('aboutus.html')


@app.route('/')
def index():

    return render_events_page(1)

@app.route('/events/<int:page>')
def events(page):
    return render_events_page(page)

def render_events_page(page):
    per_page = 6  # Number of events per page

    #connecting to the database and fetching the data
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch ticket price ranges for the dropdown
    cursor.execute("SELECT DISTINCT ticket_range FROM processed_events")
    price_ranges = [row['ticket_range'] for row in cursor.fetchall()]

    # Count total number of events
    cursor.execute("SELECT COUNT(*) FROM processed_events")
    total_events = cursor.fetchone()[0]
#=======================================
#don't ask me about the math D:, the idea is we don't know how many pages we gona need for events, 
# so this fomula basically caculate that
    # Calculate the total number of pages
    total_pages = (total_events + per_page - 1) // per_page

    # Calculate the offset for the current page
    offset = (page - 1) * per_page

    # Fetch events for the current page
    cursor.execute(f"SELECT * FROM processed_events LIMIT {per_page} OFFSET {offset}")
    events = cursor.fetchall()
#==================================================
    conn.close()

    # calculate to show or not Previous Page button
    show_previous = page > 1
    # calculate to show the Next Page button
    show_next = page < total_pages

# Render the template with the fetched events and pagination information
    return render_template('index.html', events=events, page=page, total_pages=total_pages,
                           show_previous=show_previous, show_next=show_next, price_ranges=price_ranges)

@app.route('/calendars/<filename>', methods=['GET', 'POST'])

def calendars(filename):
    filename = os.path.join("./calendars", filename + ".ics")
    return send_file(filename, as_attachment=True)

@app.route('/filter_by_price/<price_range>/<int:page>')
def filter_by_price(price_range, page):
    # Number of events to display per page
    per_page = 5
    # Establish a connection to the SQLite database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Count the total number of events for the selected price range
    cursor.execute(f"SELECT COUNT(*) FROM processed_events WHERE ticket_range = ?", (price_range,))
    total_events = cursor.fetchone()[0]

    # Calculate the total number of pages for pagination
    total_pages = (total_events + per_page - 1) // per_page

    # Calculate the offset for fetching events based on the current page
    offset = (page - 1) * per_page

    # Fetch events for the current page and the selected price range
    cursor.execute(f"SELECT * FROM processed_events WHERE ticket_range = ? LIMIT {per_page} OFFSET {offset}", (price_range,))
    filtered_events = cursor.fetchall()

    # Close the database connection
    conn.close()

    # Determine whether to show previous and next pagination links
    show_previous = page > 1
    show_next = page < total_pages

    # Render the template with the filtered events and pagination information
    return render_template('index.html', events=filtered_events, page=page, total_pages=total_pages,
                           show_previous=show_previous, show_next=show_next, selected_price_range=price_range)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
