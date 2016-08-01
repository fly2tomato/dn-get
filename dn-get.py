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
import requests

inputurl = raw_input('\n输入多瑙观看页面URL：\n')
urlFir = inputurl

#获取ASP.NET_SessionId
s=requests.Session()
url1 = 'http://www.dnvod.eu'
url2 = 'http://www.dnvod.eu/Movie/Readyplay.aspx?id=7COqHhPaRZg%3d'
s.get(url1)
r1 = s.get(url2)
header = r1.headers
rrrr = [header]
#print rrrr[0]['Set-Cookie']
reg = r'ASP.NET_SessionId=(.*); path=/; HttpOnly'
partern =  re.compile(reg)
sessionID = partern.findall(rrrr[0]['Set-Cookie'])

#构建headers
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
#ASP.NET_SessionId有时间有效性，若程序返回-4 则说明ASP.NET_SessionId已过期需要重新获取，若返回-3则表示key不对
# cookies1 = '__cfduid=d58922e790c902ec87ff7384dcfc0b2451469995023; _gat=1; ASP.NET_SessionId=2ueljjviy4takln2vcmds345; jiathis_rdc=%7B%22http%3A//www.dnvod.eu/Adult/detail.aspx%3Fid%3D0cY7CF0zIt4%253d%22%3A0%7C1469995032649%2C%22http%3A//www.dnvod.eu/Adult/Readyplay.aspx%3Fid%3D%252bJRDqHAbXxw%253d%22%3A%220%7C1469995033515%22%7D; _ga=GA1.2.733351123.1469995023'
# cookies2 = '__cfduid=d58922e790c902ec87ff7384dcfc0b2451469995023; _gat=1; ASP.NET_SessionId=2ueljjviy4takln2vcmds345; _ga=GA1.2.733351123.1469995023'
cookies = 'ASP.NET_SessionId='+sessionID[0]

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


requestFir = urllib2.Request(urlFir,None,headers)
responseFir  = urllib2.urlopen(requestFir)
data_responseFir = responseFir.read()
#print data_responseFir

para1 = urlFir[20:25]#Adult or Movie
reg     = r'id:.*\'(.*)\','
pattern = re.compile(reg)
result  = pattern.findall(data_responseFir)
para2   = result[0]

urlSec = 'http://www.dnvod.eu/'+para1+'/GetResource.ashx?id='+para2+'&type=htm'
#data = 'key=4c4e0393d0b0444cb72b0dcd9bc13417'

regkeyString = r'key:.*\'(.*)\','
patternkeyString = re.compile(regkeyString)
resultkeyString = patternkeyString.findall(data_responseFir)
keyString = resultkeyString[0]


data = urllib.urlencode({'key':keyString})
requestSec = urllib2.Request(urlSec,data,headers2)
responseSec = urllib2.urlopen(requestSec)
real_url = responseSec.read()
#print real_url
print "\nID:                 "+para2
print '\nKey:                '+keyString
print '\nASP.NET_SessionId:  '+sessionID[0]

if real_url == "-4":
    print 'ASP.NET_SessionId已过期，请重新获取'
elif real_url == "-3":
    print 'key错误，请重新设置key'
else:
    print "\n~~~~~~~~播放地址（直接复制到浏览器打开或者用迅雷下载）：~~~~~~~~\n"
    if cmp(para1,"Adult") == 0:
        pattern0 = re.compile(r'(\d||\d\d||\d_\d)\.mp4')
        num0 = re.split(pattern0,real_url)
        hdurl = num0[0]+'1'+'.mp4'+num0[2]
        if hdurl == real_url:
            print '该片为免费资源，播放地址为：\n'+hdurl+'\n'
        else:
            print '预览版: \n'+real_url+'\n'
            print '完整版: \n'+hdurl+'\n'
    else:
        pattern = re.compile(r'(\d||\d\d||\d\d\d||\d\d\d\d||\d\d\d\d\d||\d\d\d\d\d\d||\d\d\d\d\d\d\d||\d\d\d\d\d\d\d\d)\.mp4')
        num = re.split(pattern,real_url)
        hdurl = num[0]+'hd-'+num[1]+'.mp4'+num[2]
        print "低清版: \n"+real_url+'\n'
        print "高清版: \n"+hdurl+'\n'
