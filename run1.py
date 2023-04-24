from icalendar import Calendar
import html
from datetime import datetime, timedelta

import os

my_secret = os.environ['MYTOKEN']

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

def open_ics_file(filename):
    with open(filename, "rb") as f:
        data = f.read()
        cal = Calendar.from_ical(data)
        return cal

cal = open_ics_file("ics/test.ics")

events = extract_events(cal)

html_str = display_events(events)
print(html_str.encode('utf-8').decode('utf-8'))
with open('ics/output.html', 'w', encoding='utf-8') as f:
    f.write(html_str)

import requests

# 设置GitHub仓库的API地址和上传文件的路径
api_url = "https://api.github.com/repos/Daniel011011/DNS/contents/ics/output.html"
file_path = "ics/output.html"
github_token = "my_secret"

# 读取文件内容
with open(file_path, "rb") as f:
    file_content = f.read()

# 构造HTTP请求头部，包括认证信息和文件名
headers = {
    "Authorization": f"token {github_token}",
    "Content-Type": "application/json",
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "Daniel011011",
}
params = {
    "message": "upload file",
    "content": file_content.decode("utf-8"),
}

# 发送HTTP请求
response = requests.put(api_url, headers=headers, json=params)

# 打印响应结果
print(response.status_code, response.content)
