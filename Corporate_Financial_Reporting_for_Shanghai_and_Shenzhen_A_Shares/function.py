import json
import os
import random
import sys
import threading
import time
from pathlib import Path

import requests
from pyquery import PyQuery as pq

# 爬取其他页面（网易财经）所需headers
my_headers = {
    "Host": "quotes.money.163.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
    "Connection": "keep-alive",
}
# 爬取杜邦分析页面（新浪财经）所需headers
my_headers_dbfx = {
    "Host": "vip.stock.finance.sina.com.cn",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
    "Connection": "keep-alive",
}


def check_content(data_temp, url, f_run_log, f_error):
    '''
    检查有没有被反爬
    '''
    # 检测是否被反爬，如果被反爬，记录被反爬的地址并且休眠10秒
    # .text返回的是str类型，.content返回的是bytes类型
    isflag = data_temp.text.find("Forbidden")
    # 被反爬了，存错误链接
    if isflag is not -1 or len(data_temp.text) < 200:
        f_error.write(url + '\n')
        f_run_log.write(url + "\t被反爬" + '\n')
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

# 2-------------------------------------------------------------------
# 设置代理服务器（阿布云HTTP隧道专业版）


def get_proxies():
    '''代理服务器'''
    proxyHost = "http-pro.abuyun.com"
    proxyPort = "9010"

    # 代理隧道验证信息 H89329100P6Q2B4P:CA5B80409B6DA596
    proxyUser = "H89329100P6Q2B4P"
    proxyPass = "CA5B80409B6DA596"

    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host": proxyHost,
        "port": proxyPort,
        "user": proxyUser,
        "pass": proxyPass,
    }
    proxies = {
        "http": proxyMeta,
        "https": proxyMeta,
    }
    return proxies
##


def get_file(url, downloadpath, f_run_log, f_error, my_proxies):
    '''
    获取文件(zcfzb：资产负债表，lrb：利润表，xjllb：现金流量表，cwbbzy：财务报表摘要，zycwzb：主要财务数据)
    url：用于存放需爬取或下载文件的链接
    downloadpath：用于存放爬取完成后文件保存的路径
    f_run_log：运行日志文件的句柄
    f_error：运行错误日志文件的句柄（主要存放被反爬的网页链接）
    my_proxies：IP代理
    '''
    data_temp = requests.get(url, headers=my_headers,
                             proxies=my_proxies, stream=True)
    # # 检测是否被反爬，如果被反爬，记录被反爬的地址并且休眠10秒
    if check_content(data_temp, url, f_run_log, f_error) is False:
        print(url + "\t\t被反爬了")
        time.sleep(10)
    else:
        # 没被反爬，存文件
        is_file_exists(downloadpath)
        f = open(downloadpath, 'wb')  # 用二进制打开一个文件，用于读写（只能用.content来写）
        f.write(data_temp.content)
        f.close()
        f_run_log.write(url + "\t爬取成功" + '\n')
        print(url + "\t爬取成功")
    # 每访问完一次，用随机时间来休眠
    # 1-------------------------------------------------------------------
    # random_time = random.randint(2, 4)
    # time.sleep(random_time)
    # print("随机休眠了：" + str(random_time) + "秒")
    # f_run_log.write("随机休眠了：" + str(random_time) + "秒" + '\n')
    ##
    # 2-------------------------------------------------------------------
    # time.sleep(1)
    # print("休眠了：1秒")
    # f_run_log.write("休眠了：1秒" + '\n')
    ##


def get_txt_yjyg(url, downloadpath, f_run_log, f_error, my_proxies):
    # pyquery使用方法：https://blog.csdn.net/qq_36025814/article/details/90041179， https://www.cnblogs.com/lei0213/p/7676254.html
    '''
    获取需页面解析的文件(yjyg：业绩预告)
    url：用于存放需爬取或下载文件的链接
    downloadpath：用于存放爬取完成后文件保存的路径
    f_run_log：运行日志文件的句柄
    f_error：运行错误日志文件的句柄（主要存放被反爬的网页链接）
    my_proxies：IP代理
    '''
    # url = "http://quotes.money.163.com/f10/yjyg_600789.html"
    data_temp = requests.get(url, headers=my_headers,
                             proxies=my_proxies, stream=True)
    # # 检测是否被反爬，如果被反爬，记录被反爬的地址并且休眠10秒
    if check_content(data_temp, url, f_run_log, f_error) is False:
        print(url + "\t\t被反爬了")
        time.sleep(10)
    else:
        # 用pyquery解析页面
        html_data = pq(data_temp.text)
        # print(html_data)
        item = html_data('.table_bg001.border_box.table_details tr td').items()
        count = 0
        is_file_exists(downloadpath)
        f = open(downloadpath, 'w')
        # 存入文件
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
    # time.sleep(1)
    # print("休眠了：1秒")
    # f_run_log.write("休眠了：1秒" + '\n')


def get_txt_dbfx(url, downloadpath, f_run_log, f_error, my_proxies):
    # pyquery使用方法：https://blog.csdn.net/qq_36025814/article/details/90041179， https://www.cnblogs.com/lei0213/p/7676254.html
    '''
    获取需页面解析的文件(dbfx：杜邦分析)，只抓取数据（因为格式和标题都一样）
    url：用于存放需爬取或下载文件的链接
    downloadpath：用于存放爬取完成后文件保存的路径
    f_run_log：运行日志文件的句柄
    f_error：运行错误日志文件的句柄（主要存放被反爬的网页链接）
    my_proxies：IP代理

    list_event_name：每个项目的名称，如净资产收益率，净利润……
    list_report_time：存放每个公司杜邦分析的所有报告期具体时间
    list_1_1：净资产收益率的数据列表
    list_all：除净资产收益率以外的其他所有数据列表
    '''
    # url = "http://quotes.money.163.com/f10/dbfx_600519.html"
    data_temp = requests.get(url, headers=my_headers_dbfx,
                             proxies=my_proxies, stream=True)
    # # 检测是否被反爬，如果被反爬，记录被反爬的地址并且休眠10秒
    if check_content(data_temp, url, f_run_log, f_error) is False:
        print(url + "\t\t被反爬了")
        time.sleep(10)
    else:
        list_event_name = ['净资产收益率', '归属母公司股东的销售净利率', '资产周转率(次)', '权益乘数', '销售净利率', '归属母公司股东的净利润占比',
                           '营业总收入', '平均总资产', '平均总资产', '平均归属母公司股东的利益', '经营利润率', '考虑税负因素', '考虑利息负担', '归属母公司股东净利润',
                           '净利润', '期末总资产', '期末归属母公司股东的利益', 'EBIT', '净利润', '利润总额', '期初总资产', '期初归属母公司股东的利益', '营业总收入', '利润总额', 'EBIT']
        is_file_exists(downloadpath)
        list_report_time = []
        list_1_1 = []
        list_all = []
        # 网页按gb2312编码，但是python3中只有bytes才能用decode，所以用content获取bytes类型，gb2312不能满足所有要求，改用国际扩展码gbk
        html_data = pq(data_temp.content.decode('gbk'))
        # 获取每个报告期时间
        item = html_data('.datelist a').items()
        for each in item:
            list_report_time.append(each.text())
        # 获取‘净资产收益率’的数据
        item1 = html_data('.node.node-row-1 p:last-child').items()
        for each in item1:
            list_1_1.append(each.text())
        # 获取其他数据，网页中每一类数据按照行列来布局
        for row in range(6):
            for column in range(7):
                item2 = html_data('.node.node-row-' + str(row+1) +
                                  '-' + str(column+1) + ' p:last-child').items()
                # if(item2)
                for each in item2:
                    if each.text() == None:
                        break
                    else:
                        # print(each.text())
                        list_all.append(each.text())
        # 将数据写入文件，先将净资产收益率单独存入，再存入其余数据
        f = open(downloadpath, 'a+')
        f.write(url + '\n')
        for each in range(len(list_report_time)):
            f.write(list_report_time[each] + '\n')
            f.write(list_event_name[0] + ":" + list_1_1[each] + " ")
            for i in range(24):
                report_time_length = len(list_report_time)
                '''
                网页上爬下来的数据是按某一名称分类的，而写入是按某一报告期分类。
                杜邦分析每个报告期共25个数据，去掉第一个数据是单独存放的以外，其余共有24种名称的数据。
                存放的list_all列表是按照名称来存放，也就是存放了24种名称的数据。每种名称的数据共len(list_report_time)个
                所以得到求每个报告期（each），每一种名称（i）的数据公式为：i*length+each
                '''
                f.write(list_event_name[i+1] + ":" +
                        list_all[i*report_time_length+each] + " ")
            f.write('\n')
        f.close()
        f_run_log.write(url + "\t爬取成功" + '\n')
        print(url + "\t爬取成功")


'''
        爬取网易股票上每个公司的杜邦分析
        # 获取每个公司杜邦分析中所有报告期的具体时间和对应链接
        list_event_name = ['净资产收益率', '总资产收益率', '权益乘数', '销售净利率', '总资产周转率', '净利润', '营业收入',
                           '营业收入', '平均资产总额', '营业收入', '全部成本', '投资收益', '所得税', '其他', '营业成本', '销售费用', '管理费用', '财务费用']
        list_report_time = list()
        list_report_url = list()
        html_data = pq(data_temp.text)
        items = html_data('.select01 option').items()
        for each in items:
            list_report_time.append(each.text())
            list_report_url.append(each.attr('value'))
        # print(list_report_time)
        # 抓取每个报告期的数据
        thread_assemble = []  # 线程集合
        for (each_time, each_url) in zip(list_report_time, list_report_url):
            f = open(downloadpath, 'a+')  # 将文件打开为追加模式
            url_dbfx = url + "?date=" + str(each_url)  # 每个报告期的链接
            data_each_report = requests.get(
                url_dbfx, headers=my_headers, proxies=my_proxies, stream=True)
            html_data_each_report = pq(data_each_report.text)
            items_each_report = html_data_each_report('.dbbg02').items()
            f.write(each_time + '\t' + url_dbfx + "\n")  # 存每个报告期的具体时间
            # print(each_time + ":")
            for (each_figure, count) in zip(items_each_report, range(len(list_event_name))):
                f.write(list_event_name[count] + ":" + each_figure.text() + "\t")
                # print
            f.write("\n")
            # print('\n')
            f.close()
            print(each_time)
            time.sleep(0.2)
        f_run_log.write(url + "\t爬取成功" + '\n')
        print(url + "\t爬取成功")
    # time.sleep(1)
    # print("休眠了：1秒")
    # f_run_log.write("休眠了：1秒" + '\n')
'''
