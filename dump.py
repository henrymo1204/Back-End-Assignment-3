#!/usr/bin/env python3
import requests
import sys

try:
    url = sys.argv[1]
    r = requests.get(url)
    keys = r.json()
    for key in keys['keys']:
         k = requests.get(url + '/' + key)
         v = k.json()
         print(v)
except:
    print('Did not provide url')
