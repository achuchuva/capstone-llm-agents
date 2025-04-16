import icalendar
from ics import Calendar
from datetime import datetime, timedelta
from pathlib import Path
import pytz

def get_calendar():
    """Open and read the calendar file"""
    ics_path = Path("random_calendar.ics")
    with open(ics_path, 'r') as f:
        c = Calendar(f.read())

    events = []
    for e in c.events:
        events.append(f"{e.begin.strftime("%A, %B %d, %Y at %I:%M %p")}")
    formatted_events = ("\n".join(events))
    print(formatted_events)
    return formatted_events
