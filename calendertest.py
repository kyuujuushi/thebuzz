# imports
from icalendar import Calendar, Event, vText
from datetime import datetime
from pathlib import Path
import os
import pytz
 
# init the calendar
cal = Calendar()

# event stuff
event = Event()
event.add('name', 'Cool thing at UMB')
event.add('description', 'idk what it is but it sounds fun so you should go')
# time needs to be in military time and converted form est to utc
# bc for some dumbass reason it won't let me just change the time zone smh
event.add('dtstart', datetime(2023, 10, 31, 20, 0, 0, tzinfo=pytz.utc))
event.add('dtend', datetime(2023, 10, 31, 22, 0, 0, tzinfo=pytz.utc))
event['location'] = vText('Front Lawn of UMB')
cal.add_component(event)

# making of the calendar file
f = open("testCal.ics", "wb")
f.write(cal.to_ical())
f.close()
