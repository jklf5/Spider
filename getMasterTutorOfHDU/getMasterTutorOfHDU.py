import urllib.request
from lxml import etree

for m in range(6):
    url = "http://computer.hdu.edu.cn/1357/list"+str(m)+".htm"
    data = urllib.request.urlopen(url).read().decode("utf-8")
    #print(data)

    html = etree.HTML(data)
    html_data = html.xpath('/html/body/div[1]/div[5]/div[2]/div[2]/div/ul/li/a/@href')
    for i in html_data:
        url_temp = "http://computer.hdu.edu.cn" + i
        print(url_temp)
        data_temp = urllib.request.urlopen(url_temp).read().decode("utf-8")

        html_temp = etree.HTML(data_temp)
        teacher_name = html_temp.xpath('/html/body/div[1]/div[5]/div[2]/div[2]/div/h3/text()')
        print(teacher_name[0])
        
        html_data_temp = html_temp.xpath('//div[@class="wp_articlecontent"]/p/span')
        strinfo = ""
        for k in html_data_temp:
            if(k != None):
                strinfo += k.text
        print(strinfo)