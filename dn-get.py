#!/usr/bin/env python
#-*-coding:utf-8-*-
#by fly2tomato

#实现功能：
#1，获得多瑙真实播放地址，该地址可直接在浏览器中播放或者用下载工具（迅雷，you-get等）下载，屏蔽广告
#2，大福利：免费看多瑙vipAV
#使用方法：
#1，浏览器登录多瑙，进入影片播放页面，将播放页面的url复制，
#2，然后在shell运行： python dn—get.py； 回车
#3，输入复制的url，回车
#4，获得真实播放地址，
#5，对于av，获得的地址是2min预览版，请将url中的'2'换成'1'，如'cr-snyncjp-2.mp4'换成'cr-snyncjp-1.mp4'

import urllib
import httplib
import urllib2

#构建headers
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = {"User-Agent": user_agent,
"Content-Type": "application/x-www-form-urlencoded",
"Accept": "*/*",
"Referer": "http://www.dnvod.eu/Movie/Readyplay.aspx?id=2Yzcti9rYjY%3d",
"Accept-Encoding": "",
"Accept-Language": "de-DE,de;q=0.8,en-US;q=0.6,en;q=0.4,zh-CN;q=0.2,zh;q=0.2,zh-TW;q=0.2,fr-FR;q=0.2,fr;q=0.2",
"X-Requested-With": "XMLHttpRequest",
"DNT": "1",
"Cookie": "__cfduid=d88efcba63bd1bdabb48eb36678b9da0d1460149942"}

inputurl = raw_input('输入多瑙观看页面URL：\n')
urlFir = inputurl
requestFir = urllib2.Request(urlFir,None,headers)
responseFir  = urllib2.urlopen(requestFir)
data_responseFir = responseFir.read()
#print data_responseFir

locatedString_lid = "lid:"
index_lid_String = data_responseFir.index(locatedString_lid)
#print index_lid_String
start_lid = index_lid_String-35
end_lid = index_lid_String
tobefilttedstring = data_responseFir[start_lid:end_lid]
#print tobefilttedstring
locatedString_id = "id:"
locatedString_3d = "%3d"
index_id_String = tobefilttedstring.index(locatedString_id)
index_3d_String = tobefilttedstring.index(locatedString_3d)
para1 = urlFir[20:25]#Adult or Movie
#print para1
if cmp(para1,"Adult") == 0:
    start_id = index_id_String+4
else:
    start_id = index_id_String+5
end_id = index_3d_String+3
filttedstring = tobefilttedstring[start_id:end_id]#获得id
#print filttedstring

para1 = urlFir[20:25]#Adult or Movie
#print para1
para2 = filttedstring#id


urlSec = 'http://www.dnvod.eu/'+para1+'/GetResource.ashx?id='+para2+'&type=htm'

requestSec = urllib2.Request(urlSec,None,headers)
responseSec = urllib2.urlopen(requestSec)
print "\n~~~~~~~~播放地址（直接复制到浏览器打开或者用迅雷下载）：~~~~~~~~\n"+responseSec.read()
