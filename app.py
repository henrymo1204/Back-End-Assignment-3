#!/usr/bin/env python3

import sys
import logging.config

import bottle
from bottle import get, post, request, response, template, redirect

import requests
import uuid


# Set up app and logging
app = bottle.default_app()
app.config.load_config('./etc/app.ini')

logging.config.fileConfig(app.config['logging.config'])

KV_URL = app.config['sessions.kv_url']

# Disable Resource warnings produced by Bottle 0.12.19 when reloader=True
#
# See
#  <https://docs.python.org/3/library/warnings.html#overriding-the-default-filter>
#
if not sys.warnoptions:
    import warnings
    warnings.simplefilter('ignore', ResourceWarning)

sid1 = str(uuid.uuid4())
sid2 = str(uuid.uuid4())


@get('/')
def show_form():
    #count1 = request.get_cookie('count1', default='0')
    #count2 = request.get_cookie('count2', default='0')

    #count1 = int(count1) + 1

    #response.set_cookie('count1', str(count1))

    #return template('counter.tpl', counter1=count1, counter2=count2)
    
    count1 = request.get_cookie('count1')
    count2 = request.get_cookie('count2')
    if count1 is None and count2 is None:
         r = requests.put("http://localhost:5100", json={sid1: 0})
         r = requests.put("http://localhost:5100", json={sid2: 0})
    response.set_cookie('count1', sid1)
    count1 = requests.get("http://localhost:5100/" + sid1).json()[sid1]
    count2 = requests.get("http://localhost:5100/" + sid2).json()[sid2]
    count1 += 1
    requests.put("http://localhost:5100", json={sid1: count1})
    return template('counter.tpl', counter1=count1, counter2=count2)


@post('/increment')
def increment_count2():
    count2 = requests.get("http://localhost:5100/" + sid2).json()[sid2]
    count2 += 1
    r = requests.put("http://localhost:5100", json={sid2: count2})
    response.set_cookie('count2', str(count2))

    return redirect('/')


@post('/reset')
def reset_counts():
    response.delete_cookie('count1')
    response.delete_cookie('count2')

    return redirect('/')
