import requests
from pyquery import PyQuery as pq

url = "http://test.abuyun.com/proxy.php"

data_temp = requests.get(url)
html_temp = pq(data_temp.text)

item = html_temp.find("th:contains('client-ip')")

print(item.siblings().text())
