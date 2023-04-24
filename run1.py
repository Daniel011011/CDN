from icalendar import Calendar
import html
from datetime import datetime, timedelta
import os

token = os.environ['MYTOKEN']
print(token)
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


import base64
import requests

# 设置变量
file_path = "ics/output.html"
github_token = "token"
repo_owner = "Daniel011011"
repo_name = "CDN"
file_name = "output.html"
commit_message = "upload file"
print(github_token)
# 读取文件内容，并进行 base64 编码
with open(file_path, "rb") as f:
    file_content = f.read()
file_content_base64 = base64.b64encode(file_content).decode('utf-8')

# 构造 HTTP 请求头部，包括认证信息和文件名
headers = {
    "Authorization": f"token {github_token}",
    "Content-Type": "application/octet-stream",
    "User-Agent": "Daniel011011",
}

# 构造 HTTP 请求参数
params = {
    "message": commit_message,
    "content": file_content_base64,
}

# 发送 HTTP 请求
api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
response = requests.put(api_url, headers=headers, json=params)

# 检查响应状态码，确保上传成功
response.raise_for_status()
