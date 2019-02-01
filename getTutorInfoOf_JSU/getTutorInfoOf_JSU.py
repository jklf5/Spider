import urllib.request
from lxml import etree
root = "J:/allFile/Python_Project/Spider/getTutorInfoOf_JSU/Data/IMG/"

url = "http://cs.ujs.edu.cn/info/1052/5807.htm"

tr_list = []

def downloadIMG(url_img,name):
    urllib.request.urlretrieve(url_img,root+name+".jpg")

html = urllib.request.urlopen(url)
text = html.read()
text = text.decode('utf-8','ignore')
#print(text)

ehtml = etree.HTML(text)
#print(ehtml)

html_data = ehtml.xpath('//table')
for table in html_data:
    tr_list.append(table.xpath('.//tr[1]/td[3]'))

print(tr_list[0][0].text.strip())
name = tr_list[0][0].text

#下载图片
html_data_img = ehtml.xpath('//table[1]/tbody/tr[1]/td[1]/img/@src')[0]
#print(html_data_img)

url_img = "http://cs.ujs.edu.cn" + html_data_img

downloadIMG(url_img,name.strip())


