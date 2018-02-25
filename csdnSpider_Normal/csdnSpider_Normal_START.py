import urllib.request
import re

url="http://www.csdn.net/"
data=urllib.request.urlopen(url).read()
data=data.decode("utf-8","ignore")

agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
headers=(agent)
opener=urllib.request.build_opener()
opener.addheaders=[headers]

pat='href="(http://blog.csdn.net/.*?)"'
allURL=re.compile(pat).findall(data)
for i in range(0,len(allURL)):
	try:
		print("第"+str(i)+"条新闻")
		thisURL=allURL[i]
		print(thisURL)
		file="E:/allFile/Python_Project/Spider/csdnSpider_Normal/csdnNews/"+"csdnNews"+str(i)+"(2018.02.04 22.35)"+".html"
		urllib.request.urlretrieve(thisURL,file)
		print("------成功------")
	except urllib.error.URLError as e:
		if hasattr(e,"code"):
			print(e.code)
		if hasattr(e,"reason"):
			print(e.reason)