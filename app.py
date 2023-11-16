import sqlite3
from flask import Flask, render_template, request, redirect
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


if __name__ == '__main__':
    app.run()
