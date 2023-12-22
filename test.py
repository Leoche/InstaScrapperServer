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

L = instaloader.Instaloader()
profile = instaloader.Profile.from_username(L.context, "mmagramm")
json_post_list = []
for post in profile.get_posts():
    json_post_list.append(createMediaJson(post))
    break
    if len(json_post_list) > 8:
        break
returns = createJson(profile, json_post_list)
print(json.dumps(returns, indent=4))