from icalendar import Calendar
from ics import Calendar as icsCalendar
import html
from datetime import datetime, timedelta

def open_ics_file(filename):
    with open(filename, "rb") as f:
        data = f.read()
        cal = Calendar.from_ical(data)
        return cal

def extract_events(cal):
    events = []
    for component in cal.walk():
        if component.name == "VEVENT":
            event_dict = {}
            event_dict["name"] = component.get("summary")
            event_dict["start_date"] = (component.get("dtstart").dt + timedelta(hours=8)).strftime("%Y-%m-%d")
            event_dict["start_time"] = (component.get("dtstart").dt + timedelta(hours=8)).strftime("%H:%M")
            event_dict["description"] = component.get("description")
            events.append(event_dict)
    return events


def display_events(events):
    html_str = "<html><head><title>My Calendar</title></head><body>"
    html_str += "<h1>My Calendar</h1>"
    html_str += "<table border='1'>"
    html_str += "<tr><th>Date</th><th>Name</th><th>Start Time</th><th>Description</th></tr>"
    for event in events:
        html_str += "<tr>"
        html_str += f"<td>{html.escape(event['start_date'])}</td>"
        html_str += f"<td>{html.escape(event['name'])}</td>"
        html_str += f"<td>{html.escape(event['start_time'])}</td>"
        html_str += f"<td>{html.escape(event['description'])}</td>"
        html_str += "</tr>"
    html_str += "</table></body></html>"
    return html_str

def open_ics_file(filepath):
    with open(filepath, "rb") as f:
        data = f.read()
        cal = Calendar.from_ical(data)
        return cal

with open("111.txt", "w") as f:
# 写入内容
f.write("这是一个示例文件。")
    
cal = open_ics_file("ics/柯基日历订阅.ics")
events = extract_events(cal)
html_str = display_events(events)
with open('output.html', 'w', encoding='utf-8') as f:
    f.write(html_str)
