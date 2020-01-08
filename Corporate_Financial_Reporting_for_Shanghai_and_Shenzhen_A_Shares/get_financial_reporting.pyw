import os
import random
import time
from pathlib import Path

import requests
from pyquery import PyQuery as pq

import function as fun

'''
用此方法获取当运行在Corporate_Financial_Reporting_for_Shanghai_and_Shenzhen_A_Shares文件夹下时的工作路径
'''
work_cwd = os.path.abspath('..')
'''
用此方法获取当运行在Corporate_Financial_Reporting_for_Shanghai_and_Shenzhen_A_Shares上一层文件夹下时的工作路径
'''
# work_cwd = os.getcwd()
# print(work_cwd)
work_folder = 'Corporate_Financial_Reporting_for_Shanghai_and_Shenzhen_A_Shares'
path_reporting = work_cwd + \
    r'/' + work_folder + '/Financial_reporting'
path_stock_info = work_cwd + \
    r'/' + work_folder + '/Stock_info'

if __name__ == '__main__':
    stock_info_file_name = 'stock_info'  # 完整版股票信息文件名
    stock_info_unfinished_file_name = 'stock_info_unfinished'  # 未完成爬取的股票信息文件名
    stock_info_finished_file_name = 'stock_info_finished'  # 已完成爬取的股票信息文件名

    # 记录程序开始运行时间
    time_start = time.time()
    time_temp = time.localtime(time_start)
    time_start_format = time.strftime("%Y-%m-%d %H.%M.%S", time_temp)
    # 将运行产生的错误全部存入run_error_log.txt中
    fun.is_file_exists(path_reporting + '/run_error_log_' + str(time_start_format) + '.txt')
    f_error = open(path_reporting + '/run_error_log_' + str(time_start_format) + '.txt',
                   'a+')  # 打开一个文件，用于追加（非二进制打开）
    # 将运行产生的信息全部存入run_log.txt中
    fun.is_file_exists(path_reporting + '/run_log_' +
                       str(time_start_format) + '.txt')
    f_run_log = open(path_reporting + '/run_log_' +
                     str(time_start_format) + '.txt', 'a+')  # 打开一个文件，用于追加（非二进制打开）
    fun.is_first_run(f_run_log)  # 判断是否第一次运行
    # 向run_log文件中写入开始运行时间
    f_run_log.write("开始运行时间：" + str(time_start_format) + '\n')
    print("开始运行时间：" + str(time_start_format) + '\n')
    # 获取需要爬取的股票位置
    stock_info_list, stock_num_list, stock_name_list = fun.get_file_content(
        stock_info_file_name)
    stock_info_unfinished_list = fun.get_file_content(
        stock_info_unfinished_file_name)
    if len(stock_info_unfinished_list[0]) is not 0:  # 获取未完成爬取股票在完整版股票信息文件中的位置
        index = stock_info_list.index(stock_info_unfinished_list[0][1])
    else:
        index = 1
    # stock_temp_for_unfinished = stock_info_list[index-1:]

    # 开始爬取
    # for stock_index in range(20):
    for stock_index in range(index-1, len(stock_num_list)):
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
        zcfzb_path, lrb_path, xjllb_path, cwbbzy_path, yjyg_path, dbfx_path, zycwzb_path, ylnl_path, chnl_path, cznl_path, yynl_path = fun.get_file_downloadpath(stock_index)

        # 文件下载的网址(都是按报告期下载)，网址规则：http://quotes.money.163.com/service/+报告类型+股票代码+.html
        zcfzb_url, lrb_url, xjllb_url, cwbbzy_url, yjyg_url, dbfx_url, zycwzb_url, ylnl_url, chnl_url, cznl_url, yynl_url = fun.get_download_url(stock_index)

        # 爬取数据同时检查有没有被反爬(对于网易财经爬取五个休息1秒)
        fun.get_file(zcfzb_url, zcfzb_path, f_run_log, f_error, my_proxies)
        fun.get_file(lrb_url, lrb_path, f_run_log, f_error, my_proxies)
        fun.get_file(xjllb_url, xjllb_path, f_run_log, f_error, my_proxies)
        fun.get_file(cwbbzy_url, cwbbzy_path, f_run_log, f_error, my_proxies)
        fun.get_txt_yjyg(yjyg_url, yjyg_path, f_run_log, f_error, my_proxies)
        time.sleep(1)
        print("休眠了：1秒")
        f_run_log.write("休眠了：1秒" + '\n')
        fun.get_file(zycwzb_url, zycwzb_path, f_run_log, f_error, my_proxies)
        fun.get_file(ylnl_url, ylnl_path, f_run_log, f_error, my_proxies)
        fun.get_file(chnl_url, chnl_path, f_run_log, f_error, my_proxies)
        fun.get_file(cznl_url, cznl_path, f_run_log, f_error, my_proxies)
        fun.get_file(yynl_url, yynl_path, f_run_log, f_error, my_proxies)
        fun.get_txt_dbfx(dbfx_url, dbfx_path, f_run_log, f_error, my_proxies)

        # 提示信息,爬取完成只代表这个股票爬完了，但是可能存在被反爬的情况，反爬的链接存入run_error_report文件中，也可能存在“暂无数据”的情况
        f_run_log.write(display_word + "结束爬取----------" + '\n')
        print(display_word + "结束爬取----------")

        # 将未爬取的股票信息写入stock_info_unfinished.txt文件中，并将爬取完成的股票信息写入stock_info_finished.txt文件中
        stock_temp_for_unfinished = stock_info_list[stock_index + 1:]
        with open(path_stock_info + '/' + stock_info_unfinished_file_name + '.txt', 'w') as f_unfinished:
            for each in stock_temp_for_unfinished:
                f_unfinished.write(each)
        f_unfinished.close()
        with open(path_stock_info + '/' + stock_info_finished_file_name + '.txt', 'a+') as f_finished:
            # f_finished.write(
            #     stock_num_list[stock_index] + ':' + stock_name_list[stock_index] + '\n')
            f_finished.write(stock_info_list[stock_index])
        f_finished.close()
        print(stock_num_list[stock_index] + ':' +
              stock_name_list[stock_index] + '已写入stock_info_finished.txt文件中' + '\n')
        f_run_log.write(stock_num_list[stock_index] + ':' +
                        stock_name_list[stock_index] + '已写入stock_info_finished.txt文件中' + '\n')
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
