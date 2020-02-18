#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import urllib.request
port = '<div class="name">(.*?)</div>'
data = urllib.request.urlopen("https://read.douban.com/provider/all").read()
data = data.decode("utf-8")
result = re.compile(port).findall(data)
print(result)
fh = open("e:/doubanProducer.txt", "w")
for each in result:
    fh.writelines(each+"\n")
fh.close()
#
