from instagrapi import Client
from instagrapi.exceptions import LoginRequired
import logging
import http.server
import json
import argparse
import os
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qsl, urlparse, parse_qs
from dotenv import load_dotenv
import time
from pprint import pprint


load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument('--dump', nargs='?', const=8888, type=bool, default=False)
parser.add_argument('--port', nargs='?', const=8888, type=int, default=8888)
args = parser.parse_args()
PORT = args.port
DUMP = args.dump

IG_USERNAME = os.getenv('IG_USERNAME')
IG_PASSWORD = os.getenv('IG_PASSWORD')

print(IG_USERNAME)
print(IG_PASSWORD)
logger = logging.getLogger()

def createJson(profile, posts, time):
    return {
        "id":profile.pk,
        "userName":profile.username,
        "fullName":profile.full_name,
        "link":"https://www.instagram.com/" + profile.username,
        "profilePicture":str(profile.profile_pic_url),
        "medias":posts,
        "time":time
    }
def createMediaJson(post):
    return {
        "id":post.pk,
        "thumbnailSrc":str(post.thumbnail_url or post.resources[0].thumbnail_url),
        "link":"https://instagram.com/p/" + post.code,
        "date":{
            "date":post.taken_at.strftime("%Y-%m-%d %H:%M:%S")
        },
        "caption":post.caption_text,
        "video":(len(post.resources) > 0 and post.resources[0].video_url) or post.video_url is not None,
        "videoUrl": str(post.resources[0].video_url) if post.resources and len(post.resources) > 0 and post.resources[0] else str(post.video_url)
    }

def login_user():
    """
    Attempts to login to Instagram using either the provided session information
    or the provided username and password.
    """

    cl = Client()
    session = cl.load_settings("session.json")

    login_via_session = False
    login_via_pw = False

    if session:
        try:
            cl.set_settings(session)
            cl.login(IG_USERNAME, IG_PASSWORD)

            # check if session is valid
            try:
                cl.get_timeline_feed()
                print("login_via_session")
            except LoginRequired:
                print("Session is invalid, need to login via username and password")

                old_session = cl.get_settings()

                # use the same device uuids across logins
                cl.set_settings({})
                cl.set_uuids(old_session["uuids"])

                cl.login(IG_USERNAME, IG_PASSWORD)
            login_via_session = True
            print("login_via_session")
        except Exception as e:
            print("Couldn't login user using session information: %s" % e)

    if not login_via_session:
        try:
            print("Attempting to login via username and password. username: %s" % IG_USERNAME)
            if cl.login(IG_USERNAME, IG_PASSWORD):
                login_via_pw = True
                print("login_via_creds")
        except Exception as e:
            print("Couldn't login user using username and password: %s" % e)

    if not login_via_pw and not login_via_session:
        raise Exception("Couldn't login user with either password or session")
    return cl

class WebRequestHandler(BaseHTTPRequestHandler):
   def do_GET(self):
        start = time.time()
        username = parse_qs(urlparse(self.path).query).get('username', 'instagram')[0]
        if len(username) > 2:
            user = cl.user_info_by_username(username)
            print(username)
            print(user.pk)
            json_post_list = []
            for post in cl.user_medias_v1(user.pk, 12):
                json_post_list.append(createMediaJson(post))
            returns = createJson(user, json_post_list, str(time.time() - start))
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(returns, indent=4).encode("utf-8"))
        else:
            self.send_response(200)
            self.wfile.write("".encode("utf-8"))

print("DUMP:" + str(int(DUMP)));

# Init scrapper
cl = login_user()
if DUMP:
    cl.dump_settings('session.json')

# Init webserver
server_address = ("", PORT)
server = http.server.HTTPServer
handler = http.server.CGIHTTPRequestHandler
print("Listening to port:", PORT)
httpd = server(server_address, WebRequestHandler)
httpd.serve_forever()


#medias = cl.user_medias(user_id, 12)
#print(json.dumps(medias, indent=4))