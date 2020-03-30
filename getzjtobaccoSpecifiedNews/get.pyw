import requests
from pyquery import PyQuery as pq
import threading

my_headers = {
    # "Host": "flights.ctrip.com",
    "Host": "www.zjtobacco.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
    "Connection": "keep-alive",
}


def get_proxies():
    '''代理服务器，动态版'''
    proxyHost = "http-dyn.abuyun.com"
    proxyPort = "9020"

    # 代理隧道验证信息 H6343XYWC31T8O9D:5F1A3689C812C12E
    proxyUser = "H6343XYWC31T8O9D"
    proxyPass = "5F1A3689C812C12E"

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


def fun(url, my_proxies):
    response = requests.get(url, headers=my_headers,
                            proxies=my_proxies, stream=True)
    # 判断页面是否可连通
    if response.status_code != 404:
        html_temp = pq(response.content.decode('utf-8', 'ignore'))
        # 匹配不同页面的title
        if html_temp.find(".Title").text().strip() != '':
            title = html_temp.find(".Title").text()
        elif html_temp.find(".readtitle").text().strip() != '':
            title = html_temp.find(".readtitle").text()
        else:
            title = "暂无标题"
        # 指定打开的文件编码为utf-8，可以解决某些字符不能存文件的问题。
        with open("./data.txt", 'a+', encoding='utf-8') as f:
            f.write(title + '\n')
            f.write(url + '\n')
            print(title + url + "爬取完毕")
    else:
        with open('./error.txt', 'a+', encoding='utf-8') as f_error:
            f_error.write(url + '\n')


# 公告按照时间段分类，有些为隐藏公告
urlbase = "http://www.zjtobacco.com/np_file/files/release/content/"
'''urllist:用于存放构造的所有需要测试的链接
monthlist:用于存放构造链接时使用的时间
rangelist:用于存放构造链接时每个时间内的文章上下限'''
urllist = []
monthlist = [201904, 201905, 201906, 201907, 201908, 201909,
             201910, 201911, 201912, 202001, 202002, 202003]
rangelist = [107101, 107681, 108107, 108574,
             109180, 109684, 110256, 110815, 111550, 112338, 112879, 113220, 113744]
# 按照所公开公告的序号猜测所需时期内的公告为一个序号段逐一测试
'''多个时间段内链接构造'''
for month in monthlist:
    monthindex = monthlist.index(month)
    floor = rangelist[monthindex]  # 每个月对应的区间下限
    upper = rangelist[monthindex + 1]  # 每个月对应的区间上限
    for i in range(floor, upper):
        urltemp = urlbase + str(month) + "/" + str(i) + ".html"
        # print(urltemp)
        urllist.append(urltemp)
# print(len(urllist))

'''单个时间段内链接构造'''
# for i in range(106482, 107769):
#     urltemp = urlbase + str(i) + ".html"
#     urllist.append(urltemp)

for each in urllist:
    my_proxies = get_proxies()
    print("开始测试" + each)
    fun(each, my_proxies)

# fun("http://www.zjtobacco.com/np_file/files/release/content/201905/107748.html")
