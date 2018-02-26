import urllib.request as ulr
from lxml import etree
import re
import json
import string

url = "https://mp.weixin.qq.com/s/zAieVTL_svnigDrIVDUWbQ"

fault = "<p>([0-9|a-z|A-Z|\u4e00-\u9fa5].*?)<br  />"   #匹配中文字符，重要  正则在线测试工具：http://tool.chinaz.com/regex/
data = ulr.urlopen(url).read().decode("utf-8")
sourceLinkName = re.compile(fault).findall(data)
# print(sourceLinkName)

data1 = etree.HTML(data)
info = data1.xpath("//*[@id='js_content']/p/text()")
# print(info)

fh = open("D:/allFile/Python_Project/Spider/getCainiaoBaidudiskSource_Normal/data/info.txt","w",encoding="utf-8")

for no in range(1,24):
    a = info[no].split(' ',4)
    if len(a) == 4:
        fh.write(' '.join(a)+'\n')
    else:
        fh.write(' '.join(a)+'\n')

surpriseName = data1.xpath("//*[@id='js_content']/p[45]/span[2]/text()")   #单独加入“优质源码”的数据
surpriseLink = data1.xpath("//*[@id='js_content']/p[45]/text()")
fh.write(str(surpriseName[0])+'\n')
fh.write(str(surpriseLink[0])+'\n')

# surprise2 = data1.xpath("//*[@id='js_content']/p[46]/text()")  #单独加入第25个数据
# print(re.split(':|：|\n| ',surprise2[0]))
# print(len(surprise2))
# fh.write(surprise2[0]+'\n')
# fh.write(surprise2[1]+':'+surprise2[2]+':'+surprise2[3]+' '+surprise2[4]+':'+surprise2[5])

for no in range(26,43):
    a = re.split(':|：',info[no])
    fh.write(a[0]+'\n')
    b = ""
    for node in range(1,len(a)):
        b += a[node]+":"
    fh.write(b+'\n')

fh.close()