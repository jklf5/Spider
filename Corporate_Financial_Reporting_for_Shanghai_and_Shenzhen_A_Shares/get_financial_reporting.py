import requests
import time
import json
import os
import sys
import random

# 反爬
my_headers={
    "Host": "quotes.money.163.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
    "Connection": "keep-alive",
}

## 2-------------------------------------------------------------------
# 设置代理服务器（阿布云HTTP隧道专业版）
def get_proxies():
    # 代理服务器
    proxyHost = "http-pro.abuyun.com"
    proxyPort = "9010"

    # 代理隧道验证信息 H3J2I8004WDM2J2P:DD7420F8F9252166
    proxyUser = "H3J2I8004WDM2J2P"
    proxyPass = "DD7420F8F9252166"

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
##

def get_file(url, downloadpath, f_run_log, my_proxies):
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
    random_time = random.randint(2, 4)
    time.sleep(random_time)
    print("随机休眠了：" + str(random_time) + "秒")
    f_run_log.write("随机休眠了：" + str(random_time) + "秒" + '\n')

if __name__ == '__main__':
    # 记录程序开始运行时间
    time_start = time.time()
    # 将运行产生的信息全部存入run_log.txt中
    f_run_log = open('./Corporate_Financial_Reporting_for_Shanghai_and_Shenzhen_A_Shares/Financial_reporting/run_log_' + str(time_start) + '.txt', 'a+') # 打开一个文件，用于追加（非二进制打开）
    f_run_log.write("开始运行时间：" + str(time_start) + '\n')
    print("开始运行时间：" + str(time_start) + '\n')
    # 将股票的编号和名称提取出来存为两个列表
    stock_num_list = list()
    stock_name_list = list()
    f_stock_info = open('./Corporate_Financial_Reporting_for_Shanghai_and_Shenzhen_A_Shares/Stock_info/stock_info.txt', 'r') # 打开一个文件，用于只读
    stock_info = f_stock_info.readlines()
    f_stock_info.close()
    for item in stock_info:
        item = item[:-1] # 切去最后的\n
        num = item[:6] # 分割成编号
        name = item[7:] # 分割成名称
        stock_num_list.append(num)
        stock_name_list.append(name)   
    # 开始爬取
    for stock_index in range(10):
    # for stock_index in range(len(stock_num_list)):
        ## 1-------------------------------------------------------------------
        # # 每爬取10个休息10秒，每爬取50个休息60秒，每爬取100个休息120秒，每爬取1000个休息160秒
        # if stock_index is not 0:
        #     if stock_index % 1000 == 0:
        #         time.sleep(160)
        #     elif stock_index % 100 == 0:
        #         time.sleep(120)
        #     elif stock_index % 50 == 0:
        #         time.sleep(60)
        #     elif stock_index % 10 == 0:
        #         time.sleep(10)
        ##

        display_word = "----------第" + str(stock_index) + "个：" + stock_num_list[stock_index] + ":" + stock_name_list[stock_index]
        f_run_log.write(display_word + "开始爬取----------" + '\n')
        print(display_word + "开始爬取----------")
        ## 2-------------------------------------------------------------------
        # 获取代理IP并获得代理IP地址
        my_proxies = get_proxies()
        resp = requests.get("http://icanhazip.com", proxies=my_proxies)
        print("代理IP地址：" + resp.text)
        f_run_log.write("代理IP地址：" + resp.text + '\n')
        ##
        # 存放文件的路径(zcfzb：资产负债表，lrb：利润表，xjllb：现金流量表，cwbbzy：财务报表摘要，zycwzb：主要财务数据)
        zcfzb_path = './Corporate_Financial_Reporting_for_Shanghai_and_Shenzhen_A_Shares/Financial_reporting/zcfzb/' + stock_num_list[stock_index] + '_' + stock_name_list[stock_index] + '_zcfzb.csv'
        lrb_path = './Corporate_Financial_Reporting_for_Shanghai_and_Shenzhen_A_Shares/Financial_reporting/lrb/' + stock_num_list[stock_index] + '_' + stock_name_list[stock_index] + '_lrb.csv'
        xjllb_path = './Corporate_Financial_Reporting_for_Shanghai_and_Shenzhen_A_Shares/Financial_reporting/xjllb/' + stock_num_list[stock_index] + '_' + stock_name_list[stock_index] + '_xjllb.csv'
        cwbbzy_path = './Corporate_Financial_Reporting_for_Shanghai_and_Shenzhen_A_Shares/Financial_reporting/cwbbzy/' + stock_num_list[stock_index] + '_' + stock_name_list[stock_index] + '_cwbbzy.csv'
        zycwzb_path = './Corporate_Financial_Reporting_for_Shanghai_and_Shenzhen_A_Shares/Financial_reporting/zycwzb/' + stock_num_list[stock_index] + '_' + stock_name_list[stock_index] + '_zycwzb.csv'

        # 文件下载的网址(都是按报告期下载)，网址规则：http://quotes.money.163.com/service/+报告类型+股票代码+.html
        zcfzb_url = "http://quotes.money.163.com/service/zcfzb_" + stock_num_list[stock_index] + ".html"
        lrb_url = "http://quotes.money.163.com/service/lrb_" + stock_num_list[stock_index] + ".html"
        xjllb_url = "http://quotes.money.163.com/service/xjllb_" + stock_num_list[stock_index] + ".html"
        cwbbzy_url = "http://quotes.money.163.com/service/cwbbzy_" + stock_num_list[stock_index] + ".html"
        zycwzb_url = "http://quotes.money.163.com/service/zycwzb_" + stock_num_list[stock_index] + ".html?type=report"

        # 爬取数据同时检查有没有被反爬
        get_file(zcfzb_url, zcfzb_path, f_run_log, my_proxies)
        get_file(lrb_url, lrb_path, f_run_log, my_proxies)
        get_file(xjllb_url, xjllb_path, f_run_log, my_proxies)
        get_file(cwbbzy_url, cwbbzy_path, f_run_log, my_proxies)
        get_file(zycwzb_url, zycwzb_path, f_run_log, my_proxies)

        
        # 提示信息,爬取完成只代表这个股票爬完了，但是可能存在被反爬的情况，反爬的链接存入run_error_report文件中
        f_run_log.write(display_word + "结束爬取----------" + '\n')
        print(display_word + "结束爬取----------")

        # 休眠
        # 1-------------------------------------------------------------------
        # random_time = random.randint(3, 10)
        # time.sleep(random_time)
        # print("随机休眠了：" + str(random_time) + "秒")
        # f_run_log.write("随机休眠了：" + str(random_time) + "秒" + '\n')
        ##
        # 2-------------------------------------------------------------------
        time.sleep(1.5)
        print("随机休眠了：1.5秒")
        f_run_log.write("随机休眠了：1.5秒" + '\n')
        print('\n')
        f_run_log.write('\n')
        ##
    # 记录程序结束运行时间
    time_end = time.time()
    # 结算总用时
    print('totally cost',time_end-time_start)
    f_run_log.write("运行结束时间："+ str(time_end) + '\n')
    f_run_log.write("总用时：" + str(time_end-time_start) + '\n')
    f_run_log.close()