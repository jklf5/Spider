import requests
import time
import json
import os
import sys
import random
from pyquery import PyQuery as pq

my_headers={
    "Host": "quotes.money.163.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
    "Connection": "keep-alive",
}

## 2-------------------------------------------------------------------
# 设置代理服务器（阿布云HTTP隧道动态版）
def get_proxies():
    '''代理服务器'''
    proxyHost = "http-dyn.abuyun.com"
    proxyPort = "9020"

    # 代理隧道验证信息 H6343XYWC31T8O9D:5F1A3689C812C12E
    proxyUser = "H6343XYWC31T8O9D"
    proxyPass = "5F1A3689C812C12E"

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
##

def get_file(url, downloadpath, f_run_log, my_proxies):
    '''
    获取文件(zcfzb：资产负债表，lrb：利润表，xjllb：现金流量表，cwbbzy：财务报表摘要，zycwzb：主要财务数据)
    url：用于存放需爬取或下载文件的链接
    downloadpath：用于存放爬取完成后文件保存的路径
    f_run_log：运行日志文件的句柄
    my_proxies：IP代理
    '''
    data_temp = requests.get(url, headers=my_headers, proxies=my_proxies)
    # 检测是否被反爬，如果被反爬，记录被反爬的地址并且休眠15秒
    isflag = data_temp.text.find("Forbidden") # .text返回的是str类型，.content返回的是bytes类型
    # 被反爬了，存错误链接
    if isflag is not -1 or len(data_temp.content) < 200:
        print(url + "\t\t被反爬了")
        with open('./Corporate_Financial_Reporting_for_Shanghai_and_Shenzhen_A_Shares/Financial_reporting/run_error_report.txt', 'a+') as f_error: # 打开一个文件，用于追加（非二进制打开）
            f_error.write(url + '\n')
        f_error.close()
        f_run_log.write(url + "\t被反爬" + '\n')
        time.sleep(15)
    else:
    # 没被反爬，存文件
        with open(downloadpath, 'wb') as f: # 用二进制打开一个文件，用于读写（只能用.content来写）
            f.write(data_temp.content)
        f.close()
        f_run_log.write(url + "\t爬取成功" + '\n')
        print(url + "\t爬取成功")
    # 每访问完一次，用随机时间来休眠
    ## 1-------------------------------------------------------------------
    # random_time = random.randint(2, 4)
    # time.sleep(random_time)
    # print("随机休眠了：" + str(random_time) + "秒")
    # f_run_log.write("随机休眠了：" + str(random_time) + "秒" + '\n')
    ##
    ## 2-------------------------------------------------------------------
    time.sleep(1.5)
    print("休眠了：1.5秒")
    f_run_log.write("休眠了：1.5秒" + '\n')
    ##

def get_txt_yjyg(url, downloadpath, f_run_log, my_proxies):
    # pyquery使用方法：https://blog.csdn.net/qq_36025814/article/details/90041179， https://www.cnblogs.com/lei0213/p/7676254.html
    '''
    获取需页面解析的文件(yjyg：业绩预告)
    url：用于存放需爬取或下载文件的链接
    downloadpath：用于存放爬取完成后文件保存的路径
    f_run_log：运行日志文件的句柄
    my_proxies：IP代理
    '''
    # url = "http://quotes.money.163.com/f10/yjyg_600789.html"
    data_temp = requests.get(url, headers=my_headers, proxies=my_proxies)
    # 检测是否被反爬，如果被反爬，记录被反爬的地址并且休眠15秒
    isflag = data_temp.text.find("Forbidden") # .text返回的是str类型，.content返回的是bytes类型
    # 被反爬了，存错误链接
    if isflag is not -1 or len(data_temp.content) < 200:
        print(url + "\t\t被反爬了")
        with open('./Corporate_Financial_Reporting_for_Shanghai_and_Shenzhen_A_Shares/Financial_reporting/run_error_report.txt', 'a+') as f_error: # 打开一个文件，用于追加（非二进制打开）
            f_error.write(url + '\n')
        f_error.close()
        f_run_log.write(url + "\t被反爬" + '\n')
        time.sleep(15)
    else:
        ## 用pyquery解析页面
        html_data = pq(data_temp.text)
        # print(html_data)
        item = html_data('.table_bg001.border_box.table_details tr td').items()
        count = 0
        f = open(downloadpath, 'w')
        #存入文件
        for each in item:
            print(each.text())
            f.write(each.text() + '\n')
            count += 1
            if count % 10 == 0:
                f.write('\n')
        f.close()
        f_run_log.write(url + "\t爬取成功" + '\n')
        print(url + "\t爬取成功")
    time.sleep(1.5)
    print("休眠了：1.5秒")
    f_run_log.write("休眠了：1.5秒" + '\n')