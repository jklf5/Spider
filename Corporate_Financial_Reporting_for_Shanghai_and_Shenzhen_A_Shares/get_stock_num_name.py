import requests
import time
import json
import os
import sys

headers={
    "Host": "flights.ctrip.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0",
    "Referer": "http://flights.ctrip.com/booking/SHA-BJS-day-1.html?DDate1=2018-2-16",
    "Connection": "keep-alive",
}

f_stock_number = open('./Corporate_Financial_Reporting_for_Shanghai_and_Shenzhen_A_Shares/Stock_info/stock_number.txt', 'w') # 存股票代码
f_stock_name = open('./Corporate_Financial_Reporting_for_Shanghai_and_Shenzhen_A_Shares/Stock_info/stock_name.txt', 'w') # 存股票名称
f_stock_info = open('./Corporate_Financial_Reporting_for_Shanghai_and_Shenzhen_A_Shares/Stock_info/stock_info.txt', 'w') # 存股票代码+名称
for num in range(196):
    print("正在爬取第" + str(num) + "页")
    url = "http://6.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112405060379873108087_1577780463749&pn=" + str(num) + "&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152&"
    data = requests.get(url, headers=headers)
    # 将返回的string类型切片为可转换为字典类型的数据
    data_tran = data.text[118:-5]
    # 判空
    if len(data_tran) is not 0:
        data_tran = eval(data_tran) # 转化为tuple类型
        # 提取编号和名称存入stock_info中
        for data_info in data_tran:
            # print(data_info)
            # print(data_info['f12'])
            stock_number = data_info['f12']
            stock_name = data_info['f14']
            stock_info = stock_number + ":" + stock_name
            f_stock_number.writelines(stock_number + '\n')
            f_stock_name.writelines(stock_name + '\n')
            f_stock_info.writelines(stock_info + '\n')
    time.sleep(5)
f_stock_name.close()
f_stock_info.close()
f_stock_number.close()