# coding=utf-8
import requests
from pyquery import PyQuery as pq

url = "http://vip.stock.finance.sina.com.cn/corp/go.php/vFD_DupontAnalysis/stockid/002385.html"
list_report_time = []
list_1_1 = []
list_all = []
data_temp = requests.get(url)

# 网页按gb2312编码，但是python3中只有bytes才能用decode，所以用content获取bytes类型
html_data = pq(data_temp.content.decode('gb2312'))

item = html_data('.datelist a').items()
for each in item:
    list_report_time.append(each.text())
item1 = html_data('.node.node-row-1 p:last-child').items()
for each in item1:
    list_1_1.append(each.text())
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

# print(list_1_1)
# print(list_all)

list_event_name = ['净资产收益率', '归属母公司股东的销售净利率', '资产周转率(次)', '权益乘数', '销售净利率', '归属母公司股东的净利润占比',
                   '营业总收入', '平均总资产', '平均总资产', '平均归属母公司股东的利益', '经营利润率', '考虑税负因素', '考虑利息负担', '归属母公司股东净利润',
                   '净利润', '期末总资产', '期末归属母公司股东的利益', 'EBIT', '净利润', '利润总额', '期初总资产', '期初归属母公司股东的利益', '营业总收入', '利润总额', 'EBIT']

f = open("j://test.txt", 'a+')
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
