import requests
from pyquery import PyQuery as pq
import os

work_cwd = os.path.abspath('..')
path_stock_info = work_cwd + \
    r'/Corporate_Financial_Reporting_for_Shanghai_and_Shenzhen_A_Shares/Stock_info'


def f(file_name):
    stock_num_list = list()
    stock_name_list = list()
    stock_info_list = list()
    f_stock_info = open(
        path_stock_info + '/' + file_name + '.txt', 'r')  # 打开一个文件，用于只读
    stock_info_list = f_stock_info.readlines()
    f_stock_info.close()
    # stock_info = ['000631:顺发恒业\n', '600485:*ST信威\n', '002259:*ST升达\n'] #测试用
    for item in stock_info_list:
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
    return stock_info_list, stock_num_list, stock_name_list


if __name__ == "__main__":

    # 将股票的编号和名称提取出来存为两个列表
    # stock_num_list = list()
    # stock_name_list = list()
    # stock_info_list = list()
    stock_info_list, stock_num_list, stock_name_list = f('stock_info_test')
    stock_info_unfinished_list = f('stock_info_unfinished')
    # print(stock_info_list, stock_num_list, stock_name_list)
    print(stock_info_unfinished_list[0])
    if len(stock_info_unfinished_list[0]) is not 0:
        index = stock_info_list.index(stock_info_unfinished_list[0][1])
    else:
        index = 1
    # stock_temp_for_unfinished = stock_info_list[index-1:]
    for stock_index in range(index-1, len(stock_num_list)-3):
        print(stock_name_list[stock_index])
        stock_temp_for_unfinished = stock_info_list[stock_index+1:]
    with open(path_stock_info + '/test.txt', 'w') as f:
        for each in stock_temp_for_unfinished:
            f.write(each)
    f.close()
