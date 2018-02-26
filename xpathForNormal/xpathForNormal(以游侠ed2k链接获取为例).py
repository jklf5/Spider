import urllib.request
from lxml import etree #导入xpath模块

url = "http://www.soft5566.com/down/40567-1.html"

data = urllib.request(url).read().decode("utf-8")
data = data.HTML() #将request的数据转换为html内容

links = data.xpath("/html/body/div/div[2]/div/ul/li/span/a/@href/text()")

fh = open("E:/allFile/Python_Project/Spider/xpathForNormal/data/links.txt","w")

for i in range(0,len(links)):
    fh.write(links[i] + '\n')
fh.close()