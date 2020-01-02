import requests
import time
import json
import os
import sys
import random
from pyquery import PyQuery as pq
from pathlib import Path

my_headers={
    "Host": "quotes.money.163.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
    "Connection": "keep-alive",
}

def check_content(data_temp, url, f_run_log, f_error):
    '''
    检查有没有被反爬
    '''
    # 检测是否被反爬，如果被反爬，记录被反爬的地址并且休眠10秒
    isflag = data_temp.text.find("Forbidden") # .text返回的是str类型，.content返回的是bytes类型
    # 被反爬了，存错误链接
    if isflag is not -1 or len(data_temp.text) < 200:
        print(url + "\t\t被反爬了")
        f_error.write(url + '\n')
        f_run_log.write(url + "\t被反爬" + '\n')
        time.sleep(10)
        return False
    else:
        return True

def is_file_exists(downloadpath):
    '''
    判断文件是否存在，如果存在，删除；不存在，就创建
    '''
    p = Path(downloadpath)
    # print(p.exists())
    # 如果存在，则删除之
    if p.exists():
        p.unlink()
    # 如果不存在，就创建
    else:
        p.touch()

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

def get_file(url, downloadpath, f_run_log, f_error, my_proxies):
    '''
    获取文件(zcfzb：资产负债表，lrb：利润表，xjllb：现金流量表，cwbbzy：财务报表摘要，zycwzb：主要财务数据)
    url：用于存放需爬取或下载文件的链接
    downloadpath：用于存放爬取完成后文件保存的路径
    f_run_log：运行日志文件的句柄
    my_proxies：IP代理
    '''
    data_temp = requests.get(url, headers=my_headers, proxies=my_proxies)
    # # 检测是否被反爬，如果被反爬，记录被反爬的地址并且休眠15秒
    # isflag = data_temp.text.find("Forbidden") # .text返回的是str类型，.content返回的是bytes类型
    # # 被反爬了，存错误链接
    # if isflag is not -1 or len(data_temp.text) < 200:
    #     print(url + "\t\t被反爬了")
    #     with open('./Corporate_Financial_Reporting_for_Shanghai_and_Shenzhen_A_Shares/Financial_reporting/run_error_report.txt', 'a+') as f_error: # 打开一个文件，用于追加（非二进制打开）
    #         f_error.write(url + '\n')
    #     f_error.close()
    #     f_run_log.write(url + "\t被反爬" + '\n')
    #     time.sleep(15)
    if check_content(data_temp, url, f_run_log, f_error) is False:
        print("被反爬了")
    else:
    # 没被反爬，存文件
        is_file_exists(downloadpath)
        f = open(downloadpath, 'wb') # 用二进制打开一个文件，用于读写（只能用.content来写）
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
    time.sleep(1)
    print("休眠了：1秒")
    f_run_log.write("休眠了：1秒" + '\n')
    ##

def get_txt_yjyg(url, downloadpath, f_run_log, f_error, my_proxies):
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
    # # 检测是否被反爬，如果被反爬，记录被反爬的地址并且休眠15秒
    # isflag = data_temp.text.find("Forbidden") # .text返回的是str类型，.content返回的是bytes类型
    # # 被反爬了，存错误链接
    # if isflag is not -1 or len(data_temp.text) < 200:
    #     print(url + "\t\t被反爬了")
    #     with open('./Corporate_Financial_Reporting_for_Shanghai_and_Shenzhen_A_Shares/Financial_reporting/run_error_report.txt', 'a+') as f_error: # 打开一个文件，用于追加（非二进制打开）
    #         f_error.write(url + '\n')
    #     f_error.close()
    #     f_run_log.write(url + "\t被反爬" + '\n')
    #     time.sleep(15)
    if check_content(data_temp, url, f_run_log, f_error) is False:
        print("被反爬了")
    else:
        ## 用pyquery解析页面
        html_data = pq(data_temp.text)
        # print(html_data)
        item = html_data('.table_bg001.border_box.table_details tr td').items()
        count = 0
        is_file_exists(downloadpath)
        f = open(downloadpath, 'w')
        #存入文件
        for each in item:
            # print(each.text())
            f.write(each.text() + '\n')
            count += 1
            # 每个报告期数据录入完成后换行
            if count % 10 == 0:
                f.write('\n')
        f.close()
        f_run_log.write(url + "\t爬取成功" + '\n')
        print(url + "\t爬取成功")
    time.sleep(1)
    print("休眠了：1秒")
    f_run_log.write("休眠了：1秒" + '\n')

def get_txt_dbfx(url, downloadpath, f_run_log, f_error, my_proxies):
    # pyquery使用方法：https://blog.csdn.net/qq_36025814/article/details/90041179， https://www.cnblogs.com/lei0213/p/7676254.html
    '''
    获取需页面解析的文件(dbfx：杜邦分析)，只抓取数据（因为格式和标题都一样）
    url：用于存放需爬取或下载文件的链接
    downloadpath：用于存放爬取完成后文件保存的路径
    f_run_log：运行日志文件的句柄
    my_proxies：IP代理

    list_event_name：每个项目的名称，如净资产收益率，总资产收益率……
    list_report_time：存放每个公司杜邦分析的所有报告期具体时间
    list_report_url：存放每个报告期对应的链接
    url_dbfx：每个报告期对应的链接
    data_each_report：每个报告期用requests.get抓取后获得的原始页面数据
    html_data_each_report：转化为pyquery可处理的对象
    items_each_report：每个报告期中所有属性对应的键值（数据项对应的数据）
    each_figure_index：每一个数据存放的位置
    '''
    # url = "http://quotes.money.163.com/f10/dbfx_600519.html"
    data_temp = requests.get(url, headers=my_headers, proxies=my_proxies)
    # # 检测是否被反爬，如果被反爬，记录被反爬的地址并且休眠15秒
    # isflag = data_temp.text.find("Forbidden") # .text返回的是str类型，.content返回的是bytes类型
    # # 被反爬了，存错误链接
    # if isflag is not -1 or len(data_temp.text) < 200:
    #     print(url + "\t\t被反爬了")
    #     with open('./Corporate_Financial_Reporting_for_Shanghai_and_Shenzhen_A_Shares/Financial_reporting/run_error_report.txt', 'a+') as f_error: # 打开一个文件，用于追加（非二进制打开）
    #         f_error.write(url + '\n')
    #     f_error.close()
    #     f_run_log.write(url + "\t被反爬" + '\n')
    #     time.sleep(15)
    if check_content(data_temp, url, f_run_log, f_error) is False:
        print("被反爬了")
    else:
        is_file_exists(downloadpath)
        f = open(downloadpath, 'a+') #将文件打开为追加模式
        # 获取每个公司杜邦分析中所有报告期的具体时间和对应链接
        list_event_name = ['净资产收益率', '总资产收益率', '权益乘数', '销售净利率', '总资产周转率', '净利润', '营业收入', '营业收入', '平均资产总额', '营业收入', '全部成本', '投资收益', '所得税', '其他', '营业成本', '销售费用', '管理费用', '财务费用']
        list_report_time = list()
        list_report_url = list()
        html_data = pq(data_temp.text)
        items = html_data('.select01 option').items()
        for each in items:
            list_report_time.append(each.text())
            list_report_url.append(each.attr('value'))
        # print(list_report_time)
        # 抓取每个报告期的数据
        for (each_time, each_url) in zip(list_report_time, list_report_url):
            url_dbfx = url +"?date=" + str(each_url)
            data_each_report = requests.get(url_dbfx)
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
        f_run_log.write(url + "\t爬取成功" + '\n')
        print(url + "\t爬取成功")
    time.sleep(1)
    print("休眠了：1秒")
    f_run_log.write("休眠了：1秒" + '\n')