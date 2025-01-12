# chatbot_functions.py

from datetime import datetime
from sample_date import sampleData

# 1. What events are scheduled for a specific date?
def events_by_date(date):
    return [event for event in sampleData if event['dateTime'].startswith(date)]

# 2. What time are the lectures for a specific discipline?
def lectures_by_discipline(discipline):
    return [event for event in sampleData if discipline in event['discipline'] and event['type'] == 'лекции']

# 3. Which room is assigned for a specific type of event on a given date?
def room_for_event(event_type, date):
    return [event['room'] for event in sampleData if event['type'] == event_type and event['dateTime'].startswith(date)]

# 4. When are the lectures for a specific discipline?
def lecture_dates(discipline):
    return [event['dateTime'] for event in sampleData if discipline in event['discipline'] and event['type'] == 'лекции']

# 5. Which disciplines are held in a specific room?
def disciplines_in_room(room):
    return [event['discipline'] for event in sampleData if event['room'] == room]

# 6. List all events on a specific day of the week (e.g., Sunday)
def events_by_day(day_of_week):
    return [event for event in sampleData if day_of_week in event['dateTime']]

# 7. Who is the lecturer for the lectures on a specific date?
def lecturer_for_date(date):
    return [event['discipline'] for event in sampleData if event['dateTime'].startswith(date) and event['type'] == 'лекции']

# 8. What are the laboratory sessions for a specific discipline?
def laboratory_sessions(discipline):
    return [event for event in sampleData if discipline in event['discipline'] and event['type'] == 'лабораторни']

# 9. Which events are scheduled in a specific time range?
def events_in_time_range(start_time, end_time):
    result = []
    for event in sampleData:
        event_start = event['dateTime'].split(",")[1].strip().split("-")[0].strip()
        try:
            event_start_time = datetime.strptime(event_start, "%H:%M")
            if event_start_time >= datetime.strptime(start_time, "%H:%M") and event_start_time <= datetime.strptime(end_time, "%H:%M"):
                result.append(event)
        except ValueError:
            continue
    return result

# 10. List all dates for laboratory events.
def laboratory_event_dates():
    return [event['dateTime'] for event in sampleData if event['type'] == 'лабораторни']

# 1. REPONSE FORMAT What events are scheduled for a specific date?
def events_by_date(date):
    events = [event for event in sampleData if event['dateTime'].startswith(date)]
    
    # Format the response
    formatted_events = []
    for event in events:
        formatted_event = f"Event Details:\n" \
                          f" - Date and Time: {event['dateTime']}\n" \
                          f" - Discipline: {event['discipline']}\n" \
                          f" - Type: {event['type']}\n" \
                          f" - Room: {event['room']}\n"
        formatted_events.append(formatted_event)
    
    return "\n".join(formatted_events)
