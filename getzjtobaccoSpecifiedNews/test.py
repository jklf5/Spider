import requests
from pyquery import PyQuery as pq

my_headers = {
    # "Host": "flights.ctrip.com",
    "Host": "www.zjtobacco.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
    "Connection": "keep-alive",
}


def fun(url):
    response = requests.get(url, headers=my_headers)
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


urlbase = "http://www.zjtobacco.com/np_file/files/release/content/201905/"

urllist = []

for i in range(109738, 109743):
    urltemp = urlbase + str(i) + ".html"
    urllist.append(urltemp)

for each in urllist:
    print("开始测试" + each)
    fun(each)

# fun("http://www.zjtobacco.com/np_file/files/release/content/201905/107748.html")
