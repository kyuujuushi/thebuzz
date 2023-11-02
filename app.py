import sqlite3
from flask import Flask, render_template
<<<<<<< HEAD
from icalendar import Calendar, Event, vText
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

=======

app = Flask(__name__)

>>>>>>> 6b78472 (test L)
def get_db_connection():
    conn = sqlite3.connect('events.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM processed_events').fetchall()
    conn.close()
<<<<<<< HEAD



=======
>>>>>>> 6b78472 (test L)
    return render_template('index.html', posts=posts)

if __name__ == '__main__':
    app.run()
