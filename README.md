# InstaScrapper Webserver

Create a webserver, that returns without any login: **profile picture** with the latest **posts** from a **username**.

## Install

Requirements: 
- python3 
- pip3 
- Graphical server (Or Selenium compatible server)

```
pip3 install -r requirements.txt
```


## Usage

Start the server on 8888

```
python3 index.py
```

Or specify port:

```
python3 index.py --port 1337
```

Just call the server URI with a username GET parameter:

```
http://localhost:8888?username=XXX
```