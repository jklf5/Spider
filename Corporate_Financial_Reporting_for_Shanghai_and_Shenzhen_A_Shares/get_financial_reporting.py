import time
import requests
import random
import function as fun

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
        my_proxies = fun.get_proxies()
        resp = requests.get("http://icanhazip.com", proxies=my_proxies)
        print("代理IP地址：" + resp.text)
        f_run_log.write("代理IP地址：" + resp.text + '\n')
        ##

        # 存放文件的路径(zcfzb：资产负债表，lrb：利润表，xjllb：现金流量表，cwbbzy：财务报表摘要，zycwzb：主要财务数据，yjyg：业绩预告)
        zcfzb_path = './Corporate_Financial_Reporting_for_Shanghai_and_Shenzhen_A_Shares/Financial_reporting/zcfzb/' + stock_num_list[stock_index] + '_' + stock_name_list[stock_index] + '_zcfzb.csv'
        lrb_path = './Corporate_Financial_Reporting_for_Shanghai_and_Shenzhen_A_Shares/Financial_reporting/lrb/' + stock_num_list[stock_index] + '_' + stock_name_list[stock_index] + '_lrb.csv'
        xjllb_path = './Corporate_Financial_Reporting_for_Shanghai_and_Shenzhen_A_Shares/Financial_reporting/xjllb/' + stock_num_list[stock_index] + '_' + stock_name_list[stock_index] + '_xjllb.csv'
        cwbbzy_path = './Corporate_Financial_Reporting_for_Shanghai_and_Shenzhen_A_Shares/Financial_reporting/cwbbzy/' + stock_num_list[stock_index] + '_' + stock_name_list[stock_index] + '_cwbbzy.csv'
        zycwzb_path = './Corporate_Financial_Reporting_for_Shanghai_and_Shenzhen_A_Shares/Financial_reporting/zycwzb/' + stock_num_list[stock_index] + '_' + stock_name_list[stock_index] + '_zycwzb.csv'
        yjyg_path = './Corporate_Financial_Reporting_for_Shanghai_and_Shenzhen_A_Shares/Financial_reporting/yjyg/' + stock_num_list[stock_index] + '_' + stock_name_list[stock_index] + '_yjyg.txt'

        # 文件下载的网址(都是按报告期下载)，网址规则：http://quotes.money.163.com/service/+报告类型+股票代码+.html
        zcfzb_url = "http://quotes.money.163.com/service/zcfzb_" + stock_num_list[stock_index] + ".html"
        lrb_url = "http://quotes.money.163.com/service/lrb_" + stock_num_list[stock_index] + ".html"
        xjllb_url = "http://quotes.money.163.com/service/xjllb_" + stock_num_list[stock_index] + ".html"
        cwbbzy_url = "http://quotes.money.163.com/service/cwbbzy_" + stock_num_list[stock_index] + ".html"
        zycwzb_url = "http://quotes.money.163.com/service/zycwzb_" + stock_num_list[stock_index] + ".html?type=report"
        yjyg_url = "http://quotes.money.163.com/f10/yjyg_" + stock_num_list[stock_index] + ".html"

        # 爬取数据同时检查有没有被反爬
        fun.get_file(zcfzb_url, zcfzb_path, f_run_log, my_proxies)
        fun.get_file(lrb_url, lrb_path, f_run_log, my_proxies)
        fun.get_file(xjllb_url, xjllb_path, f_run_log, my_proxies)
        fun.get_file(cwbbzy_url, cwbbzy_path, f_run_log, my_proxies)
        fun.get_file(zycwzb_url, zycwzb_path, f_run_log, my_proxies)
        fun.get_txt_yjyg(yjyg_url, yjyg_path, f_run_log, my_proxies)

        
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
        print("休眠了：1.5秒")
        f_run_log.write("休眠了：1.5秒" + '\n')
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