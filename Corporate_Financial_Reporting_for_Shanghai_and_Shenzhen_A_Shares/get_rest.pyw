import os
import requests
import function as fun
import time

work_cwd = os.path.abspath('..')
work_folder = 'Corporate_Financial_Reporting_for_Shanghai_and_Shenzhen_A_Shares'
path_reporting = work_cwd + \
    r'/' + work_folder + '/Financial_reporting'
path_stock_info = work_cwd + \
    r'/' + work_folder + '/Stock_info'
stock_info_file_name = 'stock_info'  # 完整版股票信息文件名

if __name__ == "__main__":
    '''
    将被反爬的链接重新爬取，get_rest将创建新的run_log和run_error_log日志以便和正常爬取区分开

    downloadpath_for_run_log ：run_log_for_rest.txt的文件目录
    
    '''
    time_start = time.time()
    time_temp = time.localtime(time_start)
    time_start_format = time.strftime("%Y-%m-%d %H.%M.%S", time_temp)
    run_log_for_rest_file_name = "run_log_for_rest" + '_' + str(time_start_format)
    run_error_log_for_rest_file_name = "run_error_log_for_rest"
    # 打开run_error_log文件（存放被反爬的链接），获取链接
    f_rest = open(path_reporting + '/run_error_log.txt', 'r')
    # 打开run_log_for_rest文件
    downloadpath_for_run_log = path_reporting + '/' + run_log_for_rest_file_name + '.txt' 
    fun.is_file_exists(downloadpath_for_run_log)
    f_run_log_for_rest = open(downloadpath_for_run_log, 'a+')
    # 记录开始运行时间
    f_run_log_for_rest.write("开始运行时间：" + str(time_start_format) + '\n')
    print("开始运行时间：" + str(time_start_format) + '\n')
    # 打开run_error_log_for_rest文件
    downloadpath_for_run_error_log = path_reporting + '/' + run_error_log_for_rest_file_name + '.txt' 
    fun.is_file_exists("run_error_log")
    f_run_error_log_for_rest = open(downloadpath_for_run_error_log, 'a+')
    f_run_error_log_for_rest.write("开始运行时间：" + str(time_start_format) + '\n')
    # 获取stock_info.txt中的内容
    stock_info_list, stock_num_list, stock_name_list = fun.get_file_content(
        stock_info_file_name)
    rest_stock_info = f_rest.readlines()
    for each in rest_stock_info:
        each = each[:-1] # 切掉最后的'\n'
        each_num = each[-11:-5] # 从字符串中切除股票代码
        # 以股票代码从stock_info.txt文件中找到对应顺序和对应股票名称，如果是时间就跳过
        if each_num in stock_num_list:
            index = stock_num_list.index(each_num)
        else:
            continue
        each_name = stock_name_list[index]
        # print(each_name)
        # print(each_num)
        zcfzb_path, lrb_path, xjllb_path, cwbbzy_path, yjyg_path, dbfx_path, zycwzb_path, ylnl_path, chnl_path, cznl_path, yynl_path = fun.get_file_downloadpath(index)
        display_word = "----------第" + \
            str(index) + "个：" + \
            stock_num_list[index] + ":" + stock_name_list[index]
        f_run_log_for_rest.write(display_word + "开始爬取----------" + '\n')
        print(display_word + "开始爬取----------" + '\n')
        if each.find('lrb') is not -1:
            fun.get_file(each, lrb_path, f_run_log_for_rest, f_run_error_log_for_rest)
        elif each.find('Dupont') is not -1:
            fun.get_txt_dbfx(each, dbfx_path, f_run_log_for_rest, f_run_error_log_for_rest)
        elif each.find('zcfzb') is not -1:
            fun.get_file(each, zcfzb_path, f_run_log_for_rest, f_run_error_log_for_rest)
        elif each.find('xjllb') is not -1:
            fun.get_file(each, xjllb_path, f_run_log_for_rest, f_run_error_log_for_rest)
        elif each.find('cwbbzy') is not -1:
            fun.get_file(each, cwbbzy_path, f_run_log_for_rest, f_run_error_log_for_rest)
        elif each.find('yjyg') is not -1:
            fun.get_txt_yjyg(each, yjyg_path, f_run_log_for_rest, f_run_error_log_for_rest)
        elif each.find('chnl') is not -1:
            fun.get_file(each, chnl_path, f_run_log_for_rest, f_run_error_log_for_rest)
        elif each.find('cznl') is not -1:
            fun.get_file(each, cznl_path, f_run_log_for_rest, f_run_error_log_for_rest)
        elif each.find('ylnl') is not -1:
            fun.get_file(each, ylnl_path, f_run_log_for_rest, f_run_error_log_for_rest)
        elif each.find('yynl') is not -1:
            fun.get_file(each, yynl_path, f_run_log_for_rest, f_run_error_log_for_rest)
        elif each.find('zycwzb') is not -1:
            fun.get_file(each, zycwzb_path, f_run_log_for_rest, f_run_error_log_for_rest)
        f_run_log_for_rest.write(display_word + "结束爬取----------" + '\n')
        print(display_word + "结束爬取----------")
        print('\n')
    # 记录程序结束运行时间
    time_end = time.time()
    time_temp = time.localtime(time_end)
    time_end_format = time.strftime("%Y-%m-%d %H.%M.%S", time_temp)
    # 结算总用时
    print("运行结束时间：" + str(time_end_format))
    print("总用时：" + str(time_end-time_start) + "s")
    f_run_log_for_rest.write("运行结束时间：" + str(time_end_format) + '\n')
    f_run_log_for_rest.write("总用时：" + str(time_end-time_start) + '\n')
    f_run_log_for_rest.close()
    f_run_error_log_for_rest.close()
    f_rest.close()
