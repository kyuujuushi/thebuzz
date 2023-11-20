import sqlite3
from flask import Flask, render_template, request, redirect
from icalendar import Calendar, Event
from datetime import datetime
from pathlib import Path
# - Augustus
#from flask_sqlalchemy import 
# - Augustus
import os
import pytz

app = Flask(__name__, static_url_path='/static')

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
    dateList = date.split("-")

    # init the calendar
    cal = Calendar()

    #making of the event and putting it into the calendar object
    event = Event()
    event.add('name', name)
    #date is currently a dummy date will need to figure out later
    event.add('dtstart', datetime(dateList[0], dateList[1], dateList[2]).date())
    cal.add_component(event)
    # commented out currently so that we'll later figure out file shit
    # making of the calendar file
    f = open("./calendars" + name + ".ics", "wb")
    f.write(cal.to_ical())
    f.close()

def print_stuff():
    return 'hello motherfucker'

""" @app.route('/')

def index():

    '''
    # Pass the image filenames to the template
    image_filenames = [
                        'beeLogo_small non t.png', 'beeLogo_small_alpha.png'
                        'beeLogoYellow.png', 'beeLogoYellowAlphatransp.png'
                       ]
    '''
    #connecting to the database and fetching the data
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM processed_events').fetchall()

    #variables required for mk_cal function. put in the event name and date in these
    # instead of the test stuff
    #eventname = "test"
    #eventdate = 0

    #this calls mk_cal to make a .ics file for each event
        
    
    #closing of SQL
    conn.close()
    #redirecting with flask requires this code. the normal way of
    #redirecting doesn't work or else you get a 404 error which is odd but ok
    '''
    this is my attempt to redirect from one html file to another using flask
    i'll figure this out later bc its almost 9 pm and im tired ;-;
    --- kir
    '''

    return render_template('index.html', posts=posts) """

#WIP paginated (old) - Augustus
"""

    page =
request.args.get ('page', 1,
type=int)

"""

@app.route('/about')

def about():
    return render_template('aboutus.html')

'''
if request.method == 'POST':
        if request.form['aboutUs'] == 'About Us':
            redirect(url_for('aboutus.html'))
            render_template('aboutus.html', posts=posts)
'''
"""@app.route('/event')
def test():
    return render_template('event_pages.html')"""


@app.route('/')
def index():
    return render_events_page(1)

@app.route('/events/<int:page>')
def events(page):
    return render_events_page(page)

def render_events_page(page):
    per_page = 5  # Number of events per page
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch ticket price ranges for the dropdown
    cursor.execute("SELECT DISTINCT ticket_range FROM processed_events")
    price_ranges = [row['ticket_range'] for row in cursor.fetchall()]

    # Count total number of events
    cursor.execute("SELECT COUNT(*) FROM processed_events")
    total_events = cursor.fetchone()[0]
    #================================
    #Calculate the number of pages
    total_pages = (total_events + per_page - 1) // per_page
    # Calculate the offset for the current page
    offset = (page - 1) * per_page
    #=====================================
    # Fetch events for the current page
    cursor.execute(f"SELECT * FROM processed_events LIMIT {per_page} OFFSET {offset}")
    events = cursor.fetchall()

    conn.close()
# Determine whether to show previous and next pagination links
    show_previous = page > 1
    show_next = page < total_pages
# Render the template with the fetched events and pagination information
    return render_template('index.html', events=events, page=page, total_pages=total_pages,
                           show_previous=show_previous, show_next=show_next, price_ranges=price_ranges)

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
    app.run(debug=True)