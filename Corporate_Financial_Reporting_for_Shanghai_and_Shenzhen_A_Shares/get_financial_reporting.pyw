import os
import random
import time
from pathlib import Path

import requests
from pyquery import PyQuery as pq

import function as fun

if __name__ == '__main__':
    '''
    用此方法获取当运行在Corporate_Financial_Reporting_for_Shanghai_and_Shenzhen_A_Shares文件夹下时的工作路径
    '''
    work_cwd = os.path.abspath('..')
    '''
    用此方法获取当运行在Corporate_Financial_Reporting_for_Shanghai_and_Shenzhen_A_Shares上一层文件夹下时的工作路径
    '''
    # work_cwd = os.getcwd()
    # print(work_cwd)
    path_reporting = work_cwd + \
        r'/Corporate_Financial_Reporting_for_Shanghai_and_Shenzhen_A_Shares/Financial_reporting'
    path_stock_info = work_cwd + \
        r'/Corporate_Financial_Reporting_for_Shanghai_and_Shenzhen_A_Shares/Stock_info'
    # 记录程序开始运行时间
    time_start = time.time()
    time_temp = time.localtime(time_start)
    time_start_format = time.strftime("%Y-%m-%d %H.%M.%S", time_temp)
    # 将运行产生的错误全部存入run_error_log.txt中
    fun.is_file_exists(path_reporting + '/run_error_log.txt')
    f_error = open(path_reporting + '/run_error_log.txt',
                   'a+')  # 打开一个文件，用于追加（非二进制打开）
    # 将运行产生的信息全部存入run_log.txt中
    fun.is_file_exists(path_reporting + '/run_log_' +
                       str(time_start_format) + '.txt')
    f_run_log = open(path_reporting + '/run_log_' +
                     str(time_start_format) + '.txt', 'a+')  # 打开一个文件，用于追加（非二进制打开）
    f_run_log.write("开始运行时间：" + str(time_start_format) + '\n')
    print("开始运行时间：" + str(time_start_format) + '\n')
    # 将股票的编号和名称提取出来存为两个列表
    stock_num_list = list()
    stock_name_list = list()
    f_stock_info = open(
        path_stock_info + '/stock_info.txt', 'r')  # 打开一个文件，用于只读
    stock_info = f_stock_info.readlines()
    f_stock_info.close()
    # stock_info = ['000631:顺发恒业\n', '600485:*ST信威\n', '002259:*ST升达\n'] #测试用
    for item in stock_info:
        # print(item)
        item = item[:-1]  # 切去最后的\n
        num = item[:6]  # 分割成编号
        name = item[7:]  # 分割成名称
        # 股票名称中存在'*'，将*替换为^，否则在创建文件时候会出错
        flag = name.find('*')
        if flag is not -1:
            name = name.replace('*', '^')
        stock_num_list.append(num)
        stock_name_list.append(name)
    # 开始爬取
    for stock_index in range(20):
        # for stock_index in range(len(stock_num_list)):
        # 1-------------------------------------------------------------------
        # 每爬取100个休息10秒
        if stock_index is not 0:
            if stock_index % 100 == 0:
                time.sleep(10)
                print("爬满了100个，休眠了：10秒")
                f_run_log.write("爬满了100个，休眠了：10秒" + '\n')
        ##

        display_word = "----------第" + \
            str(stock_index) + "个：" + \
            stock_num_list[stock_index] + ":" + stock_name_list[stock_index]
        f_run_log.write(display_word + "开始爬取----------" + '\n')
        print(display_word + "开始爬取----------")
        # 2-------------------------------------------------------------------
        # 获取代理IP并获得代理IP地址
        my_proxies = fun.get_proxies()
        resp = requests.get("http://test.abuyun.com/proxy.php",
                            proxies=my_proxies, stream=True)
        html_temp = pq(resp.text)
        item = html_temp.find("th:contains('client-ip')")
        print("代理IP地址：" + item.siblings().text())
        f_run_log.write("代理IP地址：" + item.siblings().text() + '\n')
        ##

        # 存放文件的路径
        '''
        zcfzb资产负债表
        lrb：利润表
        xjllb：现金流量表
        cwbbzy：财务报表摘要
        yjyg：业绩预告
        dbfx：杜邦分析
        zycwzb：主要财务指标
        ylnl：盈利能力
        chnl：偿还能力
        cznl：成长能力
        yynl：营运能力
        '''
        zcfzb_path = path_reporting + '/zcfzb/' + str(stock_index) + '_' + \
            stock_num_list[stock_index] + '_' + \
            stock_name_list[stock_index] + '_zcfzb.csv'
        lrb_path = path_reporting + '/lrb/' + str(stock_index) + '_' + \
            stock_num_list[stock_index] + '_' + \
            stock_name_list[stock_index] + '_lrb.csv'
        xjllb_path = path_reporting + '/xjllb/' + str(stock_index) + '_' + \
            stock_num_list[stock_index] + '_' + \
            stock_name_list[stock_index] + '_xjllb.csv'
        cwbbzy_path = path_reporting + '/cwbbzy/' + str(stock_index) + '_' + \
            stock_num_list[stock_index] + '_' + \
            stock_name_list[stock_index] + '_cwbbzy.csv'
        yjyg_path = path_reporting + '/yjyg/' + str(stock_index) + '_' + \
            stock_num_list[stock_index] + '_' + \
            stock_name_list[stock_index] + '_yjyg.txt'
        dbfx_path = path_reporting + '/dbfx/' + str(stock_index) + '_' + \
            stock_num_list[stock_index] + '_' + \
            stock_name_list[stock_index] + '_dbfx.txt'
        zycwzb_path = path_reporting + '/zycwzb/zycwzb/' + str(stock_index) + '_' + \
            stock_num_list[stock_index] + '_' + \
            stock_name_list[stock_index] + '_zycwzb.csv'
        ylnl_path = path_reporting + '/zycwzb/ylnl/' + str(stock_index) + '_' + \
            stock_num_list[stock_index] + '_' + \
            stock_name_list[stock_index] + '_ylnl.csv'
        chnl_path = path_reporting + '/zycwzb/chnl/' + str(stock_index) + '_' + \
            stock_num_list[stock_index] + '_' + \
            stock_name_list[stock_index] + '_chnl.csv'
        cznl_path = path_reporting + '/zycwzb/cznl/' + str(stock_index) + '_' + \
            stock_num_list[stock_index] + '_' + \
            stock_name_list[stock_index] + '_cznl.csv'
        yynl_path = path_reporting + '/zycwzb/yynl/' + str(stock_index) + '_' + \
            stock_num_list[stock_index] + '_' + \
            stock_name_list[stock_index] + '_yynl.csv'

        # 文件下载的网址(都是按报告期下载)，网址规则：http://quotes.money.163.com/service/+报告类型+股票代码+.html
        zcfzb_url = "http://quotes.money.163.com/service/zcfzb_" + \
            stock_num_list[stock_index] + ".html"
        lrb_url = "http://quotes.money.163.com/service/lrb_" + \
            stock_num_list[stock_index] + ".html"
        xjllb_url = "http://quotes.money.163.com/service/xjllb_" + \
            stock_num_list[stock_index] + ".html"
        cwbbzy_url = "http://quotes.money.163.com/service/cwbbzy_" + \
            stock_num_list[stock_index] + ".html"
        yjyg_url = "http://quotes.money.163.com/f10/yjyg_" + \
            stock_num_list[stock_index] + ".html"
        dbfx_url = "http://vip.stock.finance.sina.com.cn/corp/go.php/vFD_DupontAnalysis/stockid/" + \
            stock_num_list[stock_index] + ".html"
        zycwzb_url = "http://quotes.money.163.com/service/zycwzb_" + \
            stock_num_list[stock_index] + ".html?type=report"
        ylnl_url = "http://quotes.money.163.com/service/zycwzb_" + \
            stock_num_list[stock_index] + ".html?type=report&part=ylnl"
        chnl_url = "http://quotes.money.163.com/service/zycwzb_" + \
            stock_num_list[stock_index] + ".html?type=report&part=chnl"
        cznl_url = "http://quotes.money.163.com/service/zycwzb_" + \
            stock_num_list[stock_index] + ".html?type=report&part=cznl"
        yynl_url = "http://quotes.money.163.com/service/zycwzb_" + \
            stock_num_list[stock_index] + ".html?type=report&part=yynl"

        # 爬取数据同时检查有没有被反爬
        fun.get_file(zcfzb_url, zcfzb_path, f_run_log, f_error, my_proxies)
        fun.get_file(lrb_url, lrb_path, f_run_log, f_error, my_proxies)
        fun.get_file(xjllb_url, xjllb_path, f_run_log, f_error, my_proxies)
        fun.get_file(cwbbzy_url, cwbbzy_path, f_run_log, f_error, my_proxies)
        fun.get_txt_yjyg(yjyg_url, yjyg_path, f_run_log, f_error, my_proxies)
        fun.get_file(zycwzb_url, zycwzb_path, f_run_log, f_error, my_proxies)
        fun.get_file(ylnl_url, ylnl_path, f_run_log, f_error, my_proxies)
        fun.get_file(chnl_url, chnl_path, f_run_log, f_error, my_proxies)
        fun.get_file(cznl_url, cznl_path, f_run_log, f_error, my_proxies)
        fun.get_file(yynl_url, yynl_path, f_run_log, f_error, my_proxies)
        fun.get_txt_dbfx(dbfx_url, dbfx_path, f_run_log, f_error, my_proxies)

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
        time.sleep(1)
        print("休眠了：1秒")
        f_run_log.write("休眠了：1秒" + '\n')
        print('\n')
        f_run_log.write('\n')
        ##
    # 记录程序结束运行时间
    time_end = time.time()
    time_temp = time.localtime(time_end)
    time_end_format = time.strftime("%Y-%m-%d %H.%M.%S", time_temp)
    # 结算总用时
    print("运行结束时间：" + str(time_end_format))
    print("总用时：" + str(time_end-time_start) + "s")
    f_run_log.write("运行结束时间：" + str(time_end_format) + '\n')
    f_run_log.write("总用时：" + str(time_end-time_start) + '\n')
    f_run_log.close()
    f_error.close()
