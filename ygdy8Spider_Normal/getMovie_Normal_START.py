#爬取阳光电影网站最新电影，并保存在数据库中
# -*- coding: utf-8 -*-
import urllib.request as ulr
import re
import MySQLdb
from lxml import etree

conn = MySQLdb.connect(host = '47.100.114.71',port = 3306,user = 'jklf5',passwd = 'jklf5678',db = 'movieInfo',charset = 'utf8',)#连接数据库
cur = conn.cursor()

def getList(page):
    html = ulr.urlopen('http://www.ygdy8.net/html/gndy/dyzz/list_23_%s.html' %page)
    text = html.read()#gbk > gb2312
    text = text.decode('gb2312', 'ignore') #python3必须加
    print(text)
    reg = r'<a href="(.+?)" class="ulink">(.+?)</a>'
    return re.compile(reg).findall(text)

def getContent(url):
    html = ulr.urlopen('http://www.ygdy8.net%s' %url).read()
    con_text = html.decode('gb2312', 'ignore')
    data = etree.HTML(con_text)
    reg = r'<div class="co_content8">(.+?)<p><strong><font color="#ff0000" size="4">'
    #reg = r'◎简　　介 <br /><br />\s\s(.*?)<br />'
    #reg = r'</div><div id="Zoom">([\w|\W]*?)<strong>'
    #reg = re.compile(reg,re.S)#编译正则表达式为对象,增加匹配效率
    #reg = r'<!--Content Start--><span style="FONT-SIZE: 12px"><td>([\w|\W]*)<img'
    #text = re.compile(reg).findall(con_text)
    text = re.findall(reg,con_text,re.S|re.M)
    #text = data.xpath('//*[@id="Zoom"]/span/p[1]/text()')
    if text:
        text = text[0]
        #''.join(text)  #将list转为str
        #text = text.replace('\u3000', '')
        #text = text.replace('<br>', ' ')
        #text = text.replace('<br />', ' ')
    else:
        text = ""
    reg = r'<td style="WORD-WRAP: break-word" bgcolor="#fdfddf"><a href="(.+?)"'
    link = re.findall(reg,con_text)[0]
    return text,link

for i in range(8,157):  #已爬取40页内容
    for url,title in getList(page=i):#getList()=列表[(url,标题),(url2,标题2)]
        #i=(url,标题)
        try:
            print('正在爬取第%s页的%s' %(i,title))
            content,link = getContent(url)
            print('正在保存第%s页的%s' %(i,title))
            cur.execute("insert into movie(id,title,content,link) values (NULL ,'%s' ,'%s' ,'%s')" %(title,content.replace("'",r"\'"),link))#执行sql语句
            conn.commit()
            #url,content,link都拿到了
        except Exception as e:
            print(e)

#upgrade:
# 1、测试用 [\w|\W]* 可匹配，再转换成字符串，用replace替换
# 2、测试用 r'<!--Content Start--><span style="FONT-SIZE: 12px"><td>([\w|\W]*)<img' 匹配
# 3、测试用 re.S|re.M 匹配