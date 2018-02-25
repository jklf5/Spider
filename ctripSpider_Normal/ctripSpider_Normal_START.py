# -*- coding: utf-8 -*-
import json
import urllib.request

headers={
    "Host": "flights.ctrip.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0",
    "Referer": "http://flights.ctrip.com/booking/SHA-BJS-day-1.html?DDate1=2018-2-16",
    "Connection": "keep-alive",
}

url="http://flights.ctrip.com/domesticsearch/search/SearchFirstRouteFlights?DCity1=SHA&ACity1=CTU&SearchType=S&DDate1=2018-03-02"

res=urllib.request.Request(url,headers=headers)
data=urllib.request.urlopen(res).read().decode("gb2312")#获取json数据
jsondata=json.loads(data)#将json数据解码成python字典

fh = open("E:/allFile/Python_Project/Spider/ctripSpider_Normal/data/data.json","w",encoding="utf-8")

airLineMarketingDict = {}#航空公司信息
for key in jsondata["als"]:
    airLineMarketingDict[key] = jsondata["als"][key]

spaceDict = {
    "F":"头等舱",
    "Y":"经济舱",
    "C":"公务舱",
}
i=1
for eachinfo in jsondata["fis"]:
    airLineMarketing = eachinfo["alc"]#航空公司
    takeoffOTD = json.loads(eachinfo["confort"])["HistoryPunctuality"]#出发准点率
    arriveOTD = json.loads(eachinfo["confort"])["HistoryPunctualityArr"]#到达准点率
    flightNumber = eachinfo["fn"]#航班号
    takeoffPlace = eachinfo["dpbn"]#起飞机场
    takeoffTime = eachinfo["dt"]#起飞时间
    arrivePlace = eachinfo["apbn"]#到达机场
    arriveTime = eachinfo["at"]#到达时间
    shareState = eachinfo["sdft"]#共享航班状态
    planType1 = eachinfo["cf"]["c"]#飞机型号
    planType2 = eachinfo["cf"]["dn"]#飞机型号备注
    planTypeSize = eachinfo["cf"]["s"]#飞机大小

    if (eachinfo["sts"]):
        transfer = {}  # 转机信息
        for transferlist in eachinfo["sts"]:
            transfer["转机到达时间"] = transferlist["at"]  # 转机到达时间
            transfer["转机起飞时间"] = transferlist["dt"]  # 转机起飞时间
            transfer["转机地点"] = transferlist["cn"]  # 转机地点

    basicInfo = {
        "航空公司": airLineMarketingDict.get(airLineMarketing),
        "航班号": flightNumber,
        "起飞机场": takeoffPlace,
        "起飞时间": takeoffTime,
        "达到机场": arrivePlace,
        "到达时间": arriveTime,
        "出发准点率": takeoffOTD,
        "到达准点率": arriveOTD,
        "飞机型号": planType1 + "(" + planTypeSize + ")",
        "飞机型号备注": planType2,
        "共享航班状态": shareState,
    }
    if (transfer):
        basicInfo = dict(basicInfo, **transfer)#合并字典

    fh.write('——————————————————————第'+str(i)+'个航班——————————————————'+'\n')
    #print("——————————————————————第%d个航班——————————————————" %i)
    fh.write(json.dumps(basicInfo,ensure_ascii=False)+'\n')
    #print(basicInfo)
    i += 1

    fh.writelines('——————————————————————票价信息————————————————————'+'\n')
    #print("——————————————————————票价信息————————————————————")
    priceInfo = {} #各票价信息
    for pricelist in eachinfo["scs"]:
        priceInfo["舱位类型"] = spaceDict.get(pricelist["c"])#舱位类型
        priceInfo["舱位类型备注"] = pricelist["son"]#舱位类型备注
        priceInfo["折扣"] = pricelist["rt"]#折扣
        priceInfo["票价"] = pricelist["isair"]["p"]#票价
        priceInfo["退改手续费说明"] = pricelist["tgq"]["rrn"]#退改手续费说明
        priceInfo["产品退订费包含内容"] = pricelist["tgq"]["rfn"]#产品退订费包含内容
        priceInfo["产品签转条件"] = pricelist["tgq"]["edn"]#产品签转条件
        priceInfo["产品更改费"] = pricelist["tgq"]["mef"]#产品更改费
        if (pricelist["hotel"]):
            priceInfo["机票所含酒店名称"] = pricelist["hotel"]["hn"]#机票所含酒店名称
            priceInfo["机票所含酒店地址"] = pricelist["hotel"]["ads"]#机票所含酒店地址
            priceInfo["机票所含酒店地址备注"] = pricelist["hotel"]["bd"]#机票所含酒店地址备注
            priceInfo["酒店电话"] = pricelist["hotel"]["tel"]  # 酒店电话
            priceInfo["酒店星级"] = pricelist["hotel"]["star"]  # 酒店星级
            for roomlist in pricelist["hotel"]["rooms"]:
                priceInfo["酒店房间类型"] = roomlist["name"]  # 酒店房间类型
                priceInfo["酒店房间类型备注"] = roomlist["bed"]#酒店房间类型备注
                priceInfo["入住时间"] = roomlist["ci"]#入住时间
                priceInfo["离店时间"] = roomlist["co"]#离店时间
        fh.writelines(json.dumps(priceInfo,ensure_ascii=False)+'\n')
        #print(priceInfo)

    #print("\n")

    priceInfo.clear()
    transfer.clear()

fh.close()