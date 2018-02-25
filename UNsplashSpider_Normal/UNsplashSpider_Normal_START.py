import urllib.request
import re

url="https://unsplash.com/"
data=urllib.request.urlopen(url).read().decode("utf-8","ignore")

agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
header=(agent)
opener=urllib.request.build_opener()
opener.addheaders=[header]

pat='<a href="(.*?)">'
furtherURL=re.compile(pat).findall(data)

for i in range(0,len(furtherURL)):
	try:
		print(len(furtherURL[i]))
	except urllib.error.URLError as e:
		if hasattr(e,"code"):
			print(e.code)
		if hasattr(e,"reason"):
			print(e.reason)
	except Exception as e:
		print(e)