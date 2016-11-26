#!/usr/bin/env python
# coding=utf-8
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

print '正在连接，请稍后....'

import urllib
import httplib
import urllib2
import re
import requests
import os
import sys



#��ȡASP.NET_SessionId
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

#����headers
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
#ASP.NET_SessionId��ʱ����Ч�ԣ������򷵻�-4 ��˵��ASP.NET_SessionId�ѹ�����Ҫ���»�ȡ��������-3����ʾkey����
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



loopString = True
while(loopString):
    inputArg = raw_input('1,直接输入多瑙观看页面URL，请按1\n2,搜索影片，请按2\n请输入：')
    if inputArg == '1':
        inputurl = raw_input('\n输入多瑙观看页面URL：\n')
        playUrl = inputurl
        loopString = False
    elif inputArg == '2':
        inputMovieName = raw_input('\n查找视频名称：')
        iMNUni = inputMovieName.decode('gbk')
        iMNUtf8 = iMNUni.encode('utf-8')
        if inputMovieName[0:2] == 'av':
            urlSearch = 'http://www.dnvod.eu/Adult/Search.aspx?tags='+iMNUtf8[2:len(iMNUtf8)]
            #print urlSearch
            searchRequest = urllib2.Request(urlSearch,None,headers)
            searchResponse = urllib2.urlopen(searchRequest)
            searchdataResponse = searchResponse.read()
            #print searchdataResponse
            searchReg = r'<a href="(.*%3d)">'
        else:
            urlSearch = 'http://www.dnvod.eu/Movie/Search.aspx?tags='+iMNUtf8
            searchRequest = urllib2.Request(urlSearch,None,headers)
            searchResponse = urllib2.urlopen(searchRequest)
            searchdataResponse = searchResponse.read()
            #print searchdataResponse
            searchReg = r'<a href="/\w(.*%3d)">'
        searchPattern = re.compile(searchReg)
        searchResult = searchPattern.findall(searchdataResponse)
        searchRegName = r'3d" title="(.*)">'
        searchPatternName = re.compile(searchRegName)
        searchResultName = searchPatternName.findall(searchdataResponse)
        #print searchResult
        print('\n搜索到'+str(len(searchResult))+'个结果：\n')

        for i in range(len(searchResultName)):
            print str(i+1)+': '+searchResultName[i].decode('utf-8').encode('gbk')+'\n'

        whichResultStr = raw_input('请输入数字：')
        whichResultInt = int(whichResultStr)-1

        filmIdReg = r'id=(.*%3d)'
        filmIdPattern = re.compile(filmIdReg)
        filmIdResult = filmIdPattern.findall(searchResult[whichResultInt])
        #print filmIdResult
        if inputMovieName[0:2] == 'av':
    	    searchUrl = 'http://www.dnvod.eu/Adult/detail.aspx?id='+filmIdResult[0]
        else:
    	    searchUrl = 'http://www.dnvod.eu/Movie/detail.aspx?id='+filmIdResult[0]

        #print searchUrl
        detailRequest = urllib2.Request(searchUrl,None,headers)
        #print detailRequest
        detailResponse = urllib2.urlopen(detailRequest)
        detaildataResponse = detailResponse.read()
        detailReg = r'<li><div class="bfan-n"><a href="(.*)"\s*target=".*"\s*>.*</a></div></li>'
        detailPattern = re.compile(detailReg)
        detailResult = detailPattern.findall(detaildataResponse)
        whichEpisodeStr = raw_input("一共有"+str(len(detailResult))+"集，请选择集数：")
        whichEpisodeInt = int(whichEpisodeStr)-1
        if inputMovieName[0:2] == 'av':
            playUrl = 'http://www.dnvod.eu/Adult/'+detailResult[whichEpisodeInt]
        else:
            playUrl = 'http://www.dnvod.eu'+detailResult[whichEpisodeInt]
        print '放页面URL：\n'+playUrl
        loopString = False
    else:
        print '\n输入错误，请重新输入'



requestFir = urllib2.Request(playUrl,None,headers)
#print requestFir
responseFir  = urllib2.urlopen(requestFir)
data_responseFir = responseFir.read()
#print data_responseFir

para1 = playUrl[20:25]#Adult or Movie
#print para1
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
#print "\nID:                 "+para2
#print '\nKey:                '+keyString
#print '\nASP.NET_SessionId:  '+sessionID[0]

if real_url == "-4":
    print 'ASP.NET_SessionID已过期，请重新获取'
elif real_url == "-3":
    print 'key错误，请重新设置key'
else:
    print "\n~~~~~~~~真实播放地址（直接复制到浏览器打开或者用工具下载）：~~~~~~~~\n"
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
        #print num
        hdurl = num[0]+'hd-'+num[1]+'.mp4'+num[2]
        print "低清版: \n"+real_url+'\n'
        print "高清版: \n"+hdurl+'\n'

#bDownload = raw_input('\n�Ƿ���Ҫ������Ƶ����ǰĿ¼��(y/n)')
#if bDownload == 'y':
#    os.system('axel -a -n 5 '+hdurl)
#else:
    print '\nlove & peace\n fly2tomato\n'
    raw_input('')
