#爬取阳光电影网站最新电影，并保存在数据库中
# -*- coding: utf-8 -*-
import urllib.request as ulr
import re
import MySQLdb

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
    reg = '◎简　　介 <br /><br />\s\s(.*?)<br />'
    #reg = re.compile(reg,re.S)#编译正则表达式为对象,增加匹配效率
    text = re.compile(reg).findall(con_text)
    if text:
        text = text[0]
        ''.join(text)  #将list转为str
    reg = r'<td style="WORD-WRAP: break-word" bgcolor="#fdfddf"><a href="(.+?)"'
    link = re.findall(reg,con_text)[0]
    return text,link

for i in range(1,159):
    for url,title in getList(page=i):#getList()=列表[(url,标题),(url2,标题2)]
        #i=(url,标题)
        print('正在爬取第%s页的%s' %(i,title))
        content,link = getContent(url)
        print('正在保存第%s页的%s' %(i,title))
        cur.execute("insert into movie(id,title,content,link) values (NULL ,'%s' ,'%s' ,'%s')" %(title,content.replace("'",r"\'"),link))#执行sql语句
        conn.commit()
        #url,content,link都拿到了