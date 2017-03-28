#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#import re
import os
import sys

import bottle
#from bottle import debug
from bottle import default_app, run
from bottle import request
from bottle import static_file
from bottle import jinja2_view

import steam

api = steam.WebAPI("ze api key goes here")

path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)

app = application = default_app()

@app.get('/')
@jinja2_view('index.html')
def index():
    return {}

@app.post('/')
@jinja2_view('index_result.html')
def index_result():
    sid = request.forms.get('inputid')
    sid = sid.strip("/ ")
    ssid = []
    try:
        if sid.find("steamcommunity") != -1:
            sid = sid.split('/')
            sid = sid[-1]
            if sid.isdigit():
                theid = steam.SteamID(sid)
                ssid.append(theid.as_steam2)
                ssid.append(theid.as_steam2_zero)
                ssid.append(str(theid.as_64))
                ssid.append(theid.as_steam3)
                ssid.append(theid.community_url)
                return { 'ssid': ssid, 'cond': True }
            else:
                sid = api.ISteamUser.ResolveVanityURL(vanityurl=sid)
                sid = sid['response']['steamid']
                theid = steam.SteamID(sid)
                ssid.append(theid.as_steam2)
                ssid.append(theid.as_steam2_zero)
                ssid.append(str(theid.as_64))
                ssid.append(theid.as_steam3)
                ssid.append(theid.community_url)
                return { 'ssid': ssid, 'cond': True }

        else:
            theid = steam.SteamID(sid)
            if theid.is_valid():
                ssid.append(theid.as_steam2)
                ssid.append(theid.as_steam2_zero)
                ssid.append(str(theid.as_64))
                ssid.append(theid.as_steam3)
                ssid.append(theid.community_url)

                return { 'ssid': ssid, 'cond': True }
            else:
                return {'cond': False}
    except Exception:
        return { 'cond': False }

@app.get('/about')
@jinja2_view('about.html')
def about():
    return {}

# This is used to server static files like css, images.
@app.get('/<filepath:path>')
def server_static(filepath):
    return static_file(filepath,
                       root=dir_path+'/'+'static/'
                      )

# 404 page ( ͡° ͜ʖ ͡°)
@app.error(404)
def error404(error):
    return "What are you doing here? 乁( ⁰͡ Ĺ̯ ⁰͡ ) ㄏ"


if __name__ == '__main__':
    #debug(True)
    run(app=app, host="0.0.0.0", port=8080)
