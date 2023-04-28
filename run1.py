from icalendar import Calendar
import html
import os
from datetime import datetime, timedelta
from github import Github


token = os.environ['MYTOKEN']

repo_owner = "Daniel011011"
repo_name = "calendar_kindle"

#infile需要处理的文件
infile_path = 'ics/mycal.ics'


#输出位置
outfile_path = "mycal.html"
outfile_name = "kebiao.html"



#打开文件
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
            event_dict["LOCATION"] = component.get("LOCATION")
            events.append(event_dict)
    return events
#写入html
def display_events(events):
    html_str = """<html>
<html>
    <head>
        <title>My Calendar</title>
        <style>
          p {
            font-size: 10vw; /* 字体大小为视口宽度的 5% */
          }
          th {
            font-size: 42px; /* 设置表头的字体大小为 25px */
        }
        td {
            font-size: 38px; /* 设置表格内容的字体大小为 15px */
        }
        </style>
      </head>
      
<body>
    <h1>My Calendar</h1>
    <table border='2'>
        <tr>
            <th>日期</th>
            <th>名称</th>
            <th>时间</th>
            <th>位置</th>
        </tr>"""
    for event in events:
        html_str += f"""
        <tr>
            <td>{html.escape(event['start_date'])}</td>
            <td>{html.escape(event['name'])}</td>
            <td>{html.escape(event['start_time'])}</td>
            <td>{html.escape(event['LOCATION'])}</td>
        </tr>"""
    html_str += """
    </table>
</body>
</html>"""
    return html_str



#更新文件方法
def update_github_file(file_path, token, repo_name):
    # 创建 Github 对象，使用 token 或者用户名和密码进行认证
    g = Github(token) # 或者 g = Github(login, password)

    # 获取仓库对象
    repo = g.get_user().get_repo(repo_name)

    # 构造提交信息
    commit_message = "update file by GitHubAction"

    # 获取文件内容
    with open(file_path, "rb") as f:
        file_content = f.read()

    # 获取文件的 sha 值
    contents = repo.get_contents(file_path)
    sha = contents.sha

    # 更新文件
    repo.update_file(file_path, commit_message, file_content, sha)

cal = open_ics_file(infile_path)

events = extract_events(cal)

html_str = display_events(events)

with open(outfile_path, 'w', encoding='utf-8') as f:
    f.write(html_str)

update_github_file(outfile_path,token,repo_name)
