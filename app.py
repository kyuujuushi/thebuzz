import sqlite3
from flask import Flask, render_template, request, redirect
from icalendar import Calendar, Event
from datetime import datetime
from pathlib import Path
import os
import pytz

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('events.db')
    conn.row_factory = sqlite3.Row
    return conn

def mk_cal (name, date):
    # init the calendar
    cal = Calendar()

    #making of the event and putting it into the calendar object
    event = Event()
    event.add('name', name)
    #date is currently a dummy date will need to figure out later
    event.add('dtstart', datetime(2023, 10, 31, 20, 0, 0, tzinfo=pytz.utc))
    cal.add_component(event)
    # commented out currently so that we'll later figure out file shit
    '''
    # making of the calendar file
    f = open(name + ".ics", "wb")
    f.write(cal.to_ical())
    f.close()
    '''
    return "mk_cal function has been called. this is a test"

@app.route('/')
def index():
    #connecting to the database and fetching the data
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM processed_events').fetchall()

    #variables required for mk_cal function. put in the event name and date in these
    # instead of the test stuff
    eventname = "test"
    eventdate = 0

    #closing of SQL
    conn.close()

    #flask checking for 
    if request.method == 'POST':
        if request.form['Get Calendar'] == 'getCal':
            mk_cal(eventname, eventdate)

    #redirecting with flask requires this code. the normal way of
    #redirecting doesn't work or else you get a 404 error which is odd but ok
    '''
    commenting this out because this breaks the site and causes a 400 error
    this is my attempt to redirect from one html file to another using flask
    i'll figure this out later bc its almost 9 pm and im tired ;-;
    --- kir
    if request.method == 'GET':
        if request.form['aboutUs'] == 'About Us':
            redirect(url_for('aboutus.html'))
            render_template('aboutus.html', posts=posts)
    '''

    return render_template('index.html', posts=posts)

if __name__ == '__main__':
    app.run()
