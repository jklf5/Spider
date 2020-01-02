import requests
import time
import json
import os
import sys
import random
from pyquery import PyQuery as pq
from pathlib import Path

url = "http://test.abuyun.com/proxy.php"

resp = requests.get(url)  

data = pq(resp.text)

item = data('table td:first').text()
print(item)
# for each in item:
#     print(each.text())