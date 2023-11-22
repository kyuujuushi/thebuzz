import sqlite3
from flask import *
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

    # does this stupid thing gives me strings???? yes, yes it does :)
    conn.row_factory = lambda cursor, row: row[0]

    #this calls mk_cal to make a .ics file for each event
    
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT event_name FROM processed_events
        """
    )
    eventname = cursor.fetchall()
    cursor.execute(
        """
        SELECT date FROM processed_events
        """
    )
    eventdate = cursor.fetchall()
    
    for i in range(len(eventname)):
        mk_cal(eventname[i],eventdate[i])

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

@app.route('/calendars', methods=['GET', 'POST'])

def calendars(filename):
    return url_for('calendars', filename=filename)

if __name__ == '__main__':
    app.run()
