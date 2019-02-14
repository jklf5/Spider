import requests
from lxml import etree
import getTutorInfoOf_JSU_getInfo as getinfo

urls = []
tutor_urls = []

all_url = [
    "http://cs.ujs.edu.cn/rcpy/szll/js.htm",
    "http://cs.ujs.edu.cn/rcpy/szll/js/2.htm",
    "http://cs.ujs.edu.cn/rcpy/szll/js/1.htm",
    "http://cs.ujs.edu.cn/rcpy/szll/fjs.htm",
    "http://cs.ujs.edu.cn/rcpy/szll/fjs/2.htm",
    "http://cs.ujs.edu.cn/rcpy/szll/fjs/1.htm",
    "http://cs.ujs.edu.cn/rcpy/szll/gg.htm",
]
for i in range(len(all_url)):
    url = all_url[i]
    r = requests.get(url)
    r.encoding = r.apparent_encoding
    newr = r.text
    ehtml = etree.HTML(newr)

    urls = ehtml.xpath("//ul[@class='ss']/li/a/@href")

    for i in range(len(urls)):
        each = urls[i]
        each = each.split('..')
        each_url = "http://cs.ujs.edu.cn"+each[2]
        tutor_urls.append(each_url)

for i in range(len(tutor_urls)):
    getinfo.main(tutor_urls[i])