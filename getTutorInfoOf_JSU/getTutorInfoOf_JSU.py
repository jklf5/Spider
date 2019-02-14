import urllib.request
import requests
import os
from lxml import etree
import json

root_path = os.getcwd()
# root = "J:/allFile/Python_Project/Spider/getTutorInfoOf_JSU/Data/IMG/"
path = os.path.join(root_path, "getTutorInfoOf_JSU/Data/")
# print(img_path)

url = "http://cs.ujs.edu.cn/info/1052/5807.htm"

def downloadIMG(url_img, name):
    urllib.request.urlretrieve(url_img, path+name+".jpg")

def saveInfo(all_info, name):
    fp = open(path+name+".txt", 'w', encoding='utf-8')
    for i in range(len(all_info)):
        if len(all_info[i])==2:
            fp.write(all_info[i][0])
            fp.write(all_info[i][1])
            fp.write('\n')
        else:
            fp.write(all_info[i][0])
            fp.write('\n')
            fp.write('\n')
    # with open(path+name+".json", 'w', encoding='utf-8') as json_file:
    #     json.dump(all_info, json_file, ensure_ascii=False)

# 使用urlopen请求页面，解码，封装
# html = urllib.request.urlopen(url)
# text = html.read()
# text = text.decode('utf-8','ignore')
# ehtml = etree.HTML(text)


# html_data = ehtml.xpath('//table')
# tr_list = []
# for table in html_data:
#     tr_list.append(table.xpath('.//tr[1]/td[3]'))
# print(tr_list[0][0].text.strip())
# name = tr_list[0][0].text

#使用requests请求页面，解码，替换各种标签以供后面xpath使用，最后封装为html页面
r = requests.get(url)
r.encoding = r.apparent_encoding
newr = r.text.replace(u'<BR>', u'').replace(u'<BR/>', u'')# 去除br标签
newr = newr.replace(u'<SPAN style="margin-left: 10px">', u'').replace(u'</SPAN>', u'')# 去除span标签
newr = newr.replace(u'<STRONG>', u'').replace(u'</STRONG>', u'')# 去除strong标签
# print(newr)
ehtml = etree.HTML(newr)

all_info = []
trs = ehtml.xpath('//tr')#可以直接用//text()获取全部内容
for tr in trs:
    tr_info = []
    for td in tr:
        #print(td.text)
        if td.text != None and td.text != '\r\n':   
            td.text.strip().replace(r'\u3000',r'').replace(r'\xa0',r'')#去除字符中的空格符
            td.text = ''.join(td.text.split())#对于‘\u3000’无法使用上述方法去除，只能使用该方法去除
            tr_info.append(td.text)
    if len(tr_info):    
        print(tr_info)    
        all_info.append(tr_info)

#下载图片
name = all_info[0][1]
# print(name)
html_data_img = ehtml.xpath('//table[1]/tbody/tr[1]/td[1]/img/@src')[0]
#print(html_data_img)
url_img = "http://cs.ujs.edu.cn" + html_data_img
downloadIMG(url_img, name.strip())

saveInfo(all_info, name)
