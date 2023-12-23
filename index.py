import instaloader
import json
import http.server
import argparse
from functools import cached_property
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qsl, urlparse, parse_qs


def createJson(profile, posts):
    return {
        "id":profile.userid,
        "userName":profile.username,
        "fullName":profile.full_name,
        "link":"https://www.instagram.com/" + profile.username,
        "profilePicture":profile.profile_pic_url,
        "medias":posts
    }
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

class WebRequestHandler(BaseHTTPRequestHandler):
   def do_GET(self):
        username = imsi = parse_qs(urlparse(self.path).query).get('username', 'instagram')
        L = instaloader.Instaloader(download_pictures=False, download_videos=False, download_video_thumbnails=False)
        L.load_session_from_file("defaultusernameld")
        profile = instaloader.Profile.from_username(L.context, username[0])
        json_post_list = []
        for post in profile.get_posts():
            json_post_list.append(createMediaJson(post))
            if len(json_post_list) > 8:
                break
        returns = createJson(profile, json_post_list)
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(returns, indent=4).encode("utf-8"))

parser = argparse.ArgumentParser()
parser.add_argument('--port', nargs='?', const=8888, type=int, default=8888)
args = parser.parse_args()
PORT = args.port
server_address = ("", PORT)

server = http.server.HTTPServer
handler = http.server.CGIHTTPRequestHandler
print("Listening to port:", PORT)

httpd = server(server_address, WebRequestHandler)
httpd.serve_forever()