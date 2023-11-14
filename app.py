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

@app.route('/')

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

    return render_template('index.html', posts=posts)

@app.route('/about')

def about():
    return render_template('aboutus.html')

'''
if request.method == 'POST':
        if request.form['aboutUs'] == 'About Us':
            redirect(url_for('aboutus.html'))
            render_template('aboutus.html', posts=posts)
'''
if __name__ == '__main__':
    app.run()
