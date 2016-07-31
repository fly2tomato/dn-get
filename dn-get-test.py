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
import re

#构建headers
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
#ASP.NET_SessionId有时间有效性，若程序返回-4 则说明ASP.NET_SessionId已过期需要重新获取，若返回-3则表示key不对
cookies = ' __cfduid=d88efcba63bd1bdabb48eb36678b9da0d1460149942; ASP.NET_SessionId=eiwo4m450xvunmeupdmn1q45; dn_config=device=desktop&player=CkPlayer; autologin=username=fly2tomato&userpwd=GMK1munp; dn_10534_AejJflJ1M6M%253d=11; user=vvYBilw8a4MEYoeGggfl4FQCbPPCXsclwmytrriw8ohBGSnbSHvXejqyhNjufslNXe_UqJtibBjHgfFG8yumPCmKic7_Z2p-dxFvFx6Q1FXeVA_UM6echob6iMiF3__i8OmhoCcBxI4QHuOeMpv903L0BANTrUdnZxSWMcOv6wwn8PRfKzzi2_s6K1Jd9i2B0aREoucHiyD7cTbCiJjTSioLMdaAdSsQ96E0ir4wbE6rlX7eF_9YEYPt8gqikOpogVK7cQ2; _ga=GA1.2.1028940840.1460149947'

headers = {"User-Agent": user_agent,
"Content-Type": "application/x-www-form-urlencoded",
"Accept": "*/*",
"Referer": "http://www.dnvod.eu/Movie/Readyplay.aspx?id=jydSM%2fudfCo%3d",
#"Content-Length": "36",
"Accept-Encoding": "",
"Accept-Language": "de-DE,de;q=0.8,en-US;q=0.6,en;q=0.4,zh-CN;q=0.2,zh;q=0.2,zh-TW;q=0.2,fr-FR;q=0.2,fr;q=0.2",
"X-Requested-With": "XMLHttpRequest",
"DNT": "1",
"Cookie": cookies}

headers2 = {"Host": "www.dnvod.eu",
"Content-Length": "36",
"Cache-Control": "nax-age=0",
"Accept": "*/*",
"Origin": "http://www.dnvod.eu",
"X-Requested-With": "XMLHttpRequest",
"User-Agent": user_agent,
"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
"DNT": "1",
"Referer": "http://www.dnvod.eu/Movie/Readyplay.aspx?id=%2bWXev%2bhf16w%3d",
"Accept-Encoding": "",
"Accept-Language": "de-DE,de;q=0.8,en-US;q=0.6,en;q=0.4,zh-CN;q=0.2,zh;q=0.2,zh-TW;q=0.2,fr-FR;q=0.2,fr;q=0.2",
"Connection": "keep-alive",
"Cookie": cookies}

inputurl = raw_input('输入多瑙观看页面URL：\n')
urlFir = inputurl
requestFir = urllib2.Request(urlFir,None,headers)
responseFir  = urllib2.urlopen(requestFir)
data_responseFir = responseFir.read()
#print data_responseFir

locatedString_lid = "lid:"
index_lid_String = data_responseFir.index(locatedString_lid)
print index_lid_String
start_lid = index_lid_String-35
end_lid = index_lid_String
tobefilttedstring = data_responseFir[start_lid:end_lid]
print tobefilttedstring
locatedString_id = "id:"
locatedString_3d = "%3d"
index_id_String = tobefilttedstring.index(locatedString_id)
index_3d_String = tobefilttedstring.index(locatedString_3d)
para1 = urlFir[20:25]#Adult or Movie

locatedString_key = "key:"
index_key_String = data_responseFir.index(locatedString_key)
print index_key_String
start_key = index_key_String+6
end_key = index_key_String+38
keyString = data_responseFir[start_key:end_key]
print keyString
#print para1
if cmp(para1,"Adult") == 0:
    start_id = index_id_String+4
else:
    start_id = index_id_String+5
end_id = index_3d_String+3
filttedstring = tobefilttedstring[start_id:end_id]#获得id
print filttedstring
#print para1
para2 = filttedstring#id

urlSec = 'http://www.dnvod.eu/'+para1+'/GetResource.ashx?id='+para2+'&type=htm'
#data = 'key=4c4e0393d0b0444cb72b0dcd9bc13417'

data = urllib.urlencode({'key':keyString})
requestSec = urllib2.Request(urlSec,data,headers2)
responseSec = urllib2.urlopen(requestSec)
real_url = responseSec.read()
print real_url

if real_url == "-4":
    print 'ASP.NET_SessionId已过期，请重新获取'
elif real_url == "-3":
    print 'key错误，请重新设置key'
else:
    print "\n~~~~~~~~播放地址（直接复制到浏览器打开或者用迅雷下载）：~~~~~~~~\n"
    if cmp(para1,"Adult") == 0:
        pattern0 = re.compile(r'(\d||\d\d)\.mp4')
        num0 = re.split(pattern0,real_url)
        hdurl = num0[0]+'1'+'.mp4'+num0[2]
        print '预览版: \n'+real_url
        print '完整版: \n'+hdurl
    else:
        pattern = re.compile(r'(\d||\d\d||\d\d\d||\d\d\d\d||\d\d\d\d\d||\d\d\d\d\d\d||\d\d\d\d\d\d\d||\d\d\d\d\d\d\d\d)\.mp4')
        num = re.split(pattern,real_url)
        hdurl = num[0]+'hd-'+num[1]+'.mp4'+num[2]
        print "低清版: \n"+real_url
        print "高清版: \n"+hdurl
