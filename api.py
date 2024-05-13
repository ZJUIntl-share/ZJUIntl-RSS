import os
import sys
import logging
import datetime

import requests
import flask
import waitress
import yaml
from feedgen.feed import FeedGenerator

import zjuintl_assistant

app = flask.Flask(__name__)

assist: zjuintl_assistant.Assistant = None

# middleware for logging request info
@app.after_request
def log_request_info(response):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    app.logger.info(f"{timestamp} {flask.request.method} {flask.request.url} {response.status}")
    return response

@app.route('/rss/announcements', methods=['GET'])
def get_announcements():
    fg = FeedGenerator()
    fg.id("bb_announcements")
    fg.title("Announcements")
    fg.author({"name": "ZJUIntl Assistant"})
    fg.link(href="https://learn.intl.edu.cn", rel="alternate")
    fg.description("Announcements")

    for item in assist.get_bb_announcements(50, full=True):
        fe = fg.add_entry()

        html_content = item.html_content
        if html_content is not None:
            html_content =  html_content.replace("https://learn.intl.zju.edu.cn", f"{flask.request.url_root}proxybb/https://learn.intl.zju.edu.cn")
        if (html_content is None):
            html_content = ""
            fe.id("{} {}-{}".format(item.title, item.get_event_message(), item.course))
            fe.title("{} {} - {}".format(item.title, item.get_event_message(), item.course.split(":")[0]))
        else:
            fe.id("{}-{}".format(item.title, item.course))
            fe.title("{} - {}".format(item.title, item.course.split(":")[0]))
        fe.updated(item.date.replace(tzinfo=datetime.timezone(datetime.timedelta(hours=8))))
        fe.content(html_content)

    return fg.atom_str(), 200, {"Content-Type": "application/xml"}

@app.route('/rss/grades', methods=['GET'])
def get_grades():
    fg = FeedGenerator()
    fg.id("bb_grades")
    fg.title("Grades")
    fg.author({"name": "ZJUIntl Assistant"})
    fg.link(href="https://learn.intl.zju.edu.cn", rel="alternate")
    fg.description("Grades")

    for item in assist.get_bb_grades(20):
        fe = fg.add_entry()
        fe.id(f"{item.title}-{item.course}")
        fe.title("{} - {}".format(item.title, item.course.split(":")[0]))
        fe.updated(item.date.replace(tzinfo=datetime.timezone(datetime.timedelta(hours=8))))
        fe.content(f"{item.grade} / {item.pointsPossible}")

    return fg.atom_str(), 200, {"Content-Type": "application/xml"}

@app.route('/rss/myzjunotices', methods=['GET'])
def get_myZJU_notices():
    fg = FeedGenerator()
    fg.id("myzju_notices")
    fg.title("myZJU Notices")
    fg.author({"name": "ZJUIntl Assistant"})
    fg.link(href="https://www.intl.zju.edu.cn/my-zju/zh-hans/students", rel="alternate")

    for item in assist.get_myZJU_notices(20, False, True):
        fe = fg.add_entry()
        fe.id(item.title)
        fe.title(item.title)
        fe.updated(item.date.replace(tzinfo=datetime.timezone(datetime.timedelta(hours=8))))
        fe.content(item.content)

    return fg.atom_str(), 200, {"Content-Type": "application/xml"}

@app.route('/proxybb/<path:path>', methods=['GET'])
def proxy_bb(path):
    if "learn.intl.zju.edu.cn" not in path:
        return "Invalid path", 400
    
    session = requests.Session()
    session.cookies = assist.get_cookie_jar("login_blackboard")

    response = session.get(path)

    return response.content, response.status_code, response.headers.items()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    if os.environ.get("DEBUG"):
        logging.getLogger("zjuintl_assistant.zjuintl_assistant.assistant").setLevel(logging.DEBUG)

    if not os.path.exists("config.yaml"):
        with open("config.yaml", "w") as f:
            f.write("username: \npassword: \n")
        print("Please fill in your username and password in config.yaml")
        input("Press Enter to exit ...")
        sys.exit(0)
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
        try:
            if not config["username"] or not config["password"]:
                print("Please fill in your username and password in config.yaml")
                input("Press Enter to exit ...")
                sys.exit(0)
        except KeyError:
            print("Please fill in your username and password in config.yaml")
            input("Press Enter to exit ...")
            sys.exit(0)

    assist = zjuintl_assistant.Assistant(config["username"], config["password"])

    waitress.serve(app, host='0.0.0.0', port=5000)
    