from ics import Calendar, Event
from datetime import datetime, timedelta
from pathlib import Path
from xhtml2pdf import pisa
import io
import os
import dateparser

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

def create_ics_event(name: str, start_time: str, duration: dict, location: str = "", description: str = ""):
    """Create a python dict based on the extracted event details"""
    event_data = {
        "name": name,  # title
        "description": description, # optional
        "location": location,
        "start_time": dateparser.parse(start_time),
        "duration": duration # default duration is 60 minutes if none specified 
    }
    print("Python Dict Created")
    """Open and write an event into the calendar file using the extracted event data"""
    ics_path = Path("random_calendar.ics")

    with open(ics_path, 'r') as f:
         calendar = Calendar(f.read()) # parse existing events
    print("Successfully opened calendar file for reading")
    event = Event()

    # new event data
    event.name = event_data["name"]
    event.begin = event_data["start_time"]
    event.duration = timedelta(**event_data["duration"])
    event.location = event_data["location"]
    event.description = event_data["description"]
    print("Converted event details from python dict extracted details")
    # add new event
    calendar.events.add(event)
    print("Added event details")
    with open(ics_path, 'w') as f:
        f.writelines(calendar.serialize_iter()) # writes calendar event into ics file
    
    print(f"📅 Creating: '{name}' at {start_time} for {duration} mins at {location}")

def document_creator(content: str, base_filename: str ="report") -> str:
    print("📄 DOCUMENT_CREATOR TOOL CALLED")
    print(content[:100])  # Preview
    main_content = content
    print("being called")
    script_path = os.path.abspath(__file__)

    script_directory = os.path.dirname(script_path)
    print("script directory")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"{base_filename}_{timestamp}.pdf"
    print("filename")
    output_filepath = os.path.join(script_directory, output_filename)
    print("filepath")

    source_html = io.BytesIO(content.encode("utf-8"))
    print("sourcehtml")
    with open(output_filepath, "w+b") as output_pdf:
            pisa_status = pisa.CreatePDF(
                source_html,
                dest=output_pdf
            )
    print ("open pdf")        

    if not pisa_status.err:
        return 'Document Created'
    else:
        return 'Document not created'

#create_ics_event("Q2 Marketing strategy with Jane Doe", "April 24, 2025 at 3:30 PM", {'minutes': 45}, "", "")