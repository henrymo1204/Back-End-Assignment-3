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



@get('/')
def show_form():
    #count1 = request.get_cookie('count1', default='0')
    #count2 = request.get_cookie('count2', default='0')

    #count1 = int(count1) + 1

    #response.set_cookie('count1', str(count1))

    #return template('counter.tpl', counter1=count1, counter2=count2)
    
    count = request.get_cookie('count')
    if count is None:
         sid = str(uuid.uuid4())
         requests.put("http://localhost:5100", json={sid: [0, 0]})
         count = sid
         response.set_cookie('count', count)
    c1 = requests.get("http://localhost:5100/" + count).json()[count][0]
    c2 = requests.get("http://localhost:5100/" + count).json()[count][1]
    c1 += 1
    requests.put("http://localhost:5100", json={count: [c1, c2]})
         
    return template('counter.tpl', counter1=c1, counter2=c2)


@post('/increment')
def increment_count2(): 
    #count2 = request.get_cookie('count2', default='0')
    #count2 = int(count2) + 1
    #response.set_cookie('count2', str(count2))
    count = request.get_cookie('count')
    c1 = requests.get("http://localhost:5100/" + count).json()[count][0]
    c2 = requests.get("http://localhost:5100/" + count).json()[count][1]
    c2 += 1
    requests.put("http://localhost:5100", json={count: [c1, c2]})

    return redirect('/')


@post('/reset')
def reset_counts():
    #response.delete_cookie('count1')
    #response.delete_cookie('count2')

    #return redirect('/')
    
    response.delete_cookie('count')
    delete = request.get_cookie('count')
    requests.delete("http://localhost:5100/" + delete)

    #global sid1
    #global sid2

    #sid1 = str(uuid.uuid4())
    #sid2 = str(uuid.uuid4())

    return redirect('/')
