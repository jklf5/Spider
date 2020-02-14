import json
import os
import random
import sys
import threading
import time
from pathlib import Path

import demjson
import requests
from pyquery import PyQuery as pq

# url_list = []  # 存放所有url
doc_list = []  # 存放所有doc名字
doc_url = []  # 存放所有doc的链接
count = 0
target = dict()  # 存放需要寻找的关键字的标题和链接（如所有标题中包含江苏大学的文档）
# url = "https://wenku.baidu.com/user/interface/getpgcpublicdoclist?pn=527&uname=todaytheo&uid=33825267&rn=50"

my_headers = {
    # "Host": "flights.ctrip.com",
    "Host": "wenku.baidu.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
    "Connection": "keep-alive",
}


def get(each_url):
    global count
    datatmp = requests.get(each_url, headers=my_headers, stream=True)  # 获取原始网页
    data_decode = datatmp.content.decode('unicode_escape')  # 解码
    data_decode_json = demjson.decode(data_decode)
    # data_decode_json = json.loads(data_decode)  # 转为json格式
    docs = data_decode_json['data']['doc_list']

    for each_doc in docs:
        # print(each_doc['title'])
        doc_title_tmp = each_doc['title']
        doc_list.append(doc_title_tmp)
        doc_url_tmp = "https://wenku.baidu.com/view/" + \
            each_doc['doc_id'] + ".html"
        doc_url.append(doc_url_tmp)
        count += 1
        if "江苏大学" in doc_title_tmp:
            target[doc_title_tmp] = doc_url_tmp
    print("已经完成第" + each_url + "页爬取")


if __name__ == "__main__":
    for i in range(1, 856):
        if i % 100 == 0:
            time.sleep(5)
            print("爬满100个，休眠5秒")
        else:
            url_tmp = "https://wenku.baidu.com/user/interface/getpgcpublicdoclist?pn=" + \
                str(i) + "&uname=todaytheo&uid=33825267&rn=50"
            # url_list.append(url_tmp)
            get(url_tmp)

    # get(url)
    # 进一步筛选
    for each_item in target.items():
        if "操作系统" in each_item[0]:
            print(each_item)
    # print(target)
    print(count)
