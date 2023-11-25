import sqlite3
from flask import *
from icalendar import Calendar, Event
from datetime import datetime
from pathlib import Path
import os
import pytz

app = Flask(__name__)

#add location later
def mk_cal (name, date):
    # init the calendar
    cal = Calendar()
    
    # event stuff
    event = Event()
    event.add('name', name)
    #date needs to be converted from string to numbers
    event.add('dtstart', datetime(2023, 10, 31, 20, 0, 0, tzinfo=pytz.utc))
    cal.add_component(event)
    '''
    f = open("testCal.ics", "wb")
    f.write(cal.to_ical())
    f.close()
    '''

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
    per_page = 5  # Number of events per page

    #connecting to the database and fetching the data
    conn = get_db_connection()
    cursor = conn.cursor()

    # Count total number of events, coount #rows
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

    return render_template('index.html', events=events, page=page, total_pages=total_pages,show_previous=show_previous, show_next=show_next)


@app.route('/calendars/<filename>', methods=['GET', 'POST'])

def calendars(filename):
    filename = os.path.join("./calendars", filename + ".ics")
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run()
