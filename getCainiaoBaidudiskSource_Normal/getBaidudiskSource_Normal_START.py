import urllib.request as ulr
from lxml import etree
import re

url = "https://mp.weixin.qq.com/s/zAieVTL_svnigDrIVDUWbQ"

fault = "<p>([0-9|a-z|A-Z|\u4e00-\u9fa5].*?)<br  />"   #匹配中文字符，重要  正则在线测试工具：http://tool.chinaz.com/regex/
data = ulr.urlopen(url).read().decode("utf-8")
sourceLinkName = re.compile(fault).findall(data)
# print(sourceLinkName)

data1 = etree.HTML(data)
name = data1.xpath("//*[@id='js_content']/p/text()")

for no in range(1,len(name)):
    a = name[no].split("链接:")
    print(a)
# for infoNO in range(0,len(sourceLinkName),2):
#     print(sourceLinkName[infoNO])