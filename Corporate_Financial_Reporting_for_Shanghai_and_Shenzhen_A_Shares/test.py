import requests
import time
import json
import os
import sys
import random
from pyquery import PyQuery as pq
from pathlib import Path
import threading
import threadpool
from multiprocessing import Pool
from functools import partial
# from pathos.multiprocessing import ProcessingPool as Pool

mutex = threading.Lock()
sem = threading.Semaphore(3)
time_start = time.time()
class my_thread(threading.Thread):
    def __init__(self, url, each_time, each_url, downloadpath, list_event_name, my_proxies):
    # def __init__(self, url, each_time, each_url, downloadpath, list_event_name):
        super(my_thread, self).__init__ ()
        self.url = url
        self.each_time = each_time
        self.each_url = each_url
        self.downloadpath = downloadpath
        self.list_event_name = list_event_name
        self.my_proxies = my_proxies
    def run(self):
        # f(self.url, self.each_time, self.each_url, self.downloadpath, self.list_event_name, self.my_proxies)
        f(self.url, self.each_time, self.each_url, self.downloadpath)

my_headers={
    "Host": "quotes.money.163.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
    "Connection": "keep-alive",
}

def get_proxies():
    '''代理服务器'''
    proxyHost = "http-pro.abuyun.com"
    proxyPort = "9010"

    # 代理隧道验证信息 H89329100P6Q2B4P:CA5B80409B6DA596
    proxyUser = "H89329100P6Q2B4P"
    proxyPass = "CA5B80409B6DA596"

    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
      "host" : proxyHost,
      "port" : proxyPort,
      "user" : proxyUser,
      "pass" : proxyPass,
    }
    proxies = {
        "http"  : proxyMeta,
        "https" : proxyMeta,
    }
    return proxies

# def f(url, each_time, each_url, downloadpath, my_proxies):
def f(url, each_time, each_url, downloadpath):
    # 抓取每个报告期的数据
    # for (each_time, each_url) in zip(list_report_time, list_report_url):
    # with sem:
        # if mutex.acquire(1):
    list_event_name = ['净资产收益率', '总资产收益率', '权益乘数', '销售净利率', '总资产周转率', '净利润', '营业收入', '营业收入', '平均资产总额', '营业收入', '全部成本', '投资收益', '所得税', '其他', '营业成本', '销售费用', '管理费用', '财务费用']
    f = open(downloadpath, 'a+') #将文件打开为追加模式
    url_dbfx = url +"?date=" + str(each_url) # 每个报告期的链接
    # data_each_report = requests.get(url_dbfx, headers=my_headers, proxies=my_proxies, stream=True)
    data_each_report = requests.get(url_dbfx, headers=my_headers, stream=True)
    html_data_each_report = pq(data_each_report.text)
    items_each_report = html_data_each_report('.dbbg02').items()
    f.write(each_time + '\t' + url_dbfx + "\n") #存每个报告期的具体时间
    # print(each_time + ":")
    for (each_figure, count) in zip(items_each_report, range(len(list_event_name))):
        f.write(list_event_name[count] + ":" + each_figure.text() + "\t")
        # print
    f.write("\n")
    # print('\n')
    f.close()
    print(each_time)
    # time.sleep(0.2)
    # mutex.release()

my_proxies = get_proxies()

url = "http://quotes.money.163.com/f10/dbfx_000955.html"

work_cwd = os.path.abspath('..') 

path_reporting = work_cwd + r'/Corporate_Financial_Reporting_for_Shanghai_and_Shenzhen_A_Shares/Financial_reporting'

# data_temp = requests.get(url, headers=my_headers, proxies=my_proxies, stream=True)
data_temp = requests.get(url, headers=my_headers, stream=True)
downloadpath = path_reporting + '/test_dbfx.txt'

list_report_time = list()
list_report_url = list()
html_data = pq(data_temp.text)
items = html_data('.select01 option').items()
for each in items:
    list_report_time.append(each.text())
    list_report_url.append(each.attr('value'))
# print(list_report_time)

# thread_assemble = []
# for (each_time, each_url) in zip(list_report_time, list_report_url):
#     t = my_thread(url, each_time, each_url, downloadpath, list_event_name, my_proxies)
#     # t = my_thread(url, each_time, each_url, downloadpath, list_event_name)
#     print(t.getName())
#     t.start()
#     # t.join()
#     # thread_assemble.append(t)

# # for thread in thread_assemble:
#     # print(threading.current_thread().name)
#     # thread.join()
# requests_pool_list = []
pool = threadpool.ThreadPool(3)
# for (each_time, each_url) in zip(list_report_time, list_report_url):
#     requests_pool_each = threadpool.makeRequests(f, args_list=[url, each_time, each_url, downloadpath, list_event_name])
#     requests_pool_list.append(requests_pool_each)
arguments = []
for (each_time, each_url) in zip(list_report_time, list_report_url):
    dict_temp = {'url':url, 'each_time':each_time, 'each_url':each_url, 'downloadpath':downloadpath}
    arguments_temp = (None, dict_temp)
    arguments.append(arguments_temp)
# print(arguments)
requests_pool = threadpool.makeRequests(f, arguments)
# map(pool.putRequest, requests_pool_list)
# for req in requests_pool:
#     pool.putRequest(req)
[pool.putRequest(req) for req in requests_pool] 
pool.wait()
time_end = time.time()
print(time_end-time_start)

