import instaloader
import json
import http.server
import argparse
from functools import cached_property
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qsl, urlparse, parse_qs



class WebRequestHandler(BaseHTTPRequestHandler):
   def do_GET(self):
        username = imsi = parse_qs(urlparse(self.path).query).get('username', 'instagram')

        L = instaloader.Instaloader()
        profile = instaloader.Profile.from_username(L.context, username[0])
        json_post_list = []
        for post in profile.get_posts():
            print("post")
            json_post_list.append(instaloader.get_json_structure(post).get("node"))
            if len(json_post_list) > 8:
                break
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(json_post_list).encode("utf-8"))


parser = argparse.ArgumentParser()
parser.add_argument('--port', nargs='?', const=8888, type=int)
args = parser.parse_args()
PORT = args.port
server_address = ("", PORT)

server = http.server.HTTPServer
handler = http.server.CGIHTTPRequestHandler
print("Listening to port:", PORT)

httpd = server(server_address, WebRequestHandler)
httpd.serve_forever()