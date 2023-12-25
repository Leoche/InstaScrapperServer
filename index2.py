from instagrapi import Client
from instagrapi.exceptions import LoginRequired
import logging
import json
import argparse
import os
from dotenv import load_dotenv

load_dotenv()

IG_USERNAME = os.getenv('IG_USERNAME')
IG_PASSWORD = os.getenv('IG_PASSWORD')

print(IG_USERNAME)
print(IG_PASSWORD)
logger = logging.getLogger()
def createMediaJson(post):
    return {
        "id":post.mediaid,
        "thumbnailSrc":instaloader.get_json_structure(post).get("node").get("thumbnail_src"),
        "link":"https://instagram.com/p/" + post.shortcode,
        "date":{
            "date":post.date_utc.strftime("%Y-%m-%d %H:%M:%S")
        },
        "caption":post.caption,
        "video":post.is_video,
        "videoUrl":post.video_url
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

parser = argparse.ArgumentParser()
parser.add_argument('--dump', nargs='?', const=8888, type=bool, default=False)
args = parser.parse_args()
DUMP = args.dump
print("DUMP:" + DUMP);

cl = login_user()
if DUMP:
    cl.dump_settings('session.json')
user_id = cl.user_id_from_username("mmagramm")
print(user_id)
medias = cl.user_medias(user_id, 12)
#print(json.dumps(medias, indent=4))