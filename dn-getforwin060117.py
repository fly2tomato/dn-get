# !/usr/bin/env python
#-*-coding:utf-8-*-
#by fly2tomato

#实现功能：
#1，获得多瑙真实播放地址，该地址可直接在浏览器中播放或者用下载工具（迅雷，you-get等）下载，屏蔽广告
#2，大福利：免费看多瑙vipAV
#使用方法：
#1，浏览器登录多瑙，进入影片播放页面，将播放页面的url复制，
#2，然后在shell运行： python dn—get.py； 回车
#3，输入复制的url，回车
#5，对于av，获得的地址是2min预览版，请将url中的'2'换成'1'，如'cr-snyncjp-2.mp4'换成'cr-snyncjp-1.mp4'
#4，获得真实播放地址，
#import cookielib
import urllib
#import httplib
import urllib2
import re
import requests
import os
#import sys
#import time
#from selenium import webdriver
#from bs4 import BeautifulSoup

url1 = 'http://www.dnvod.eu/'
url2 = 'http://www.dnvod.eu/Movie/Readyplay.aspx?id=9Qm2PeBpd5s%3d'

def main(playUrl,headers):
    real_url = get_real_url(playUrl,headers)
    #print real_url
    data_responseFir = get_html_content(playUrl,headers)
    para1 = playUrl[20:25]#Adult or Movie
    #print para1
    para2 = regular_process(r'id:.*\'(.*)\',',data_responseFir)[0]
    #print "\nID:                 "+para2
    #print '\nKey:                '+keyString
    #print '\nASP.NET_SessionId:  '+sessionID
    if real_url == "-4":
        print 'ASP.NET_SessionID已过期，请重新获取'.decode('utf-8').encode('gbk')
    elif real_url == "-3":
        print 'key错误，请重新设置key'.decode('utf-8').encode('gbk')
    else:
        hdurl = hdurl_print(real_url,para1,para2)
    bDownload = raw_input('\n是否需要下载视频到当前目录(for mac and linux only)？(y/n)'.decode('utf-8').encode('gbk'))
    if bDownload == 'y':
        os.system('axel -a -n 5 '+hdurl)
    else:
        isPlay = raw_input('\n是否需要在线播放该视频(for mac and linux only)？(y/n)'.decode('utf-8').encode('gbk'))
        if isPlay == 'y':
            os.system('mplayer '+hdurl)
        else:
            print '\nlove & peace\nfly2tomato\n'

def hdurl_print(real_url,para1,para2):
    print "\n********真实播放地址（直接复制到浏览器打开或者用工具下载）：********\n".decode('utf-8').encode('gbk')
    if cmp(para1,"Adult") == 0:
        pattern0 = re.compile(r'(\d||\d\d||\d_\d)\.mp4')
        num0 = re.split(pattern0,real_url)
        hdurl = num0[0]+'1'+'.mp4'+num0[2]
        if hdurl == real_url:
            print '该片为免费资源，播放地址为：\n'+hdurl+'\n'.decode('utf-8').encode('gbk')
        else:
            print '预览版: \n'+real_url+'\n'.decode('utf-8').encode('gbk')
            print '完整版: \n'+hdurl+'\n'.decode('utf-8').encode('gbk')
    else:
        pattern = re.compile(r'(\d||\d\d||\d\d\d||\d\d\d\d||\d\d\d\d\d||\d\d\d\d\d\d||\d\d\d\d\d\d\d||\d\d\d\d\d\d\d\d)\.mp4')
        num = re.split(pattern,real_url)
        #print num
        #print "低清版: \n"+real_url+'\n'
        hdurl0 = num[0] + 'hd-' + num[1] + '.mp4' + num[2]
        hdurl = getHDRealUrl(hdurl0,real_url)
        print " 高清版: \n".decode('utf-8').encode('gbk')+hdurl+'\n'.decode('utf-8').encode('gbk')
    return hdurl

def get_real_url(playUrl,headers):
    data_responseFir = get_html_content(playUrl,headers)
    para1 = playUrl[20:25]#Adult or Movie
    para2 = regular_process(r'id:.*\'(.*)\',',data_responseFir)[0]
    urlSec = 'http://www.dnvod.eu/'+para1+'/GetResource.ashx?id='+para2+'&type=htm'
    keyString = regular_process(r'key:.*\'(.*)\',',data_responseFir)[0]
    data = urllib.urlencode({'key':keyString})
    requestSec = urllib2.Request(urlSec,data,headers)
    responseSec = urllib2.urlopen(requestSec)
    real_url = responseSec.read()
    return real_url

def get_play_url(searchUrl,headers):
    detail_content = get_html_content(searchUrl,headers)
    episode_list = regular_process(r'Readyplay.aspx\?id=(.*)" target',detail_content)
    totalEps = len(episode_list)
    #print detailResult
    whichEpisodeStr = raw_input("一共有".decode('utf-8').encode('gbk')+str(totalEps)+"集，请选择集数：".decode('utf-8').encode('gbk'))
    whichEpisodeInt = int(whichEpisodeStr)-1
    try:
        if inputMovieName[0:2] == 'av':
            playUrl = 'http://www.dnvod.eu/Adult/Readyplay.aspx?id='+episode_list[whichEpisodeInt]
            return playUrl
        else:
            playUrl = 'http://www.dnvod.eu/Movie/Readyplay.aspx?id='+episode_list[whichEpisodeInt]
            return playUrl
    except:
        playUrl = 'http://www.dnvod.eu/Movie/Readyplay.aspx?id='+episode_list[whichEpisodeInt]
        return playUrl

def suibiankankan(channel_url,total_num):
    html_content = get_html_content(channel_url, headers)
    match_movie_address = r'<a href="(.*%3d)">'
    movie_address_list = regular_process(match_movie_address, html_content)
    match_movie_name = r'%3d" title="(.*)">'
    movie_name_list = regular_process(match_movie_name, html_content)
    del movie_name_list[35]
    del movie_name_list[36]
    del movie_name_list[37]
    match_movie_popular = r'color:#FD2525\'>(.*)</font>'
    movie_popular_list = regular_process(match_movie_popular, html_content)
    # print len(movie_address_list)
    # print len(movie_name_list)
    # print len(movie_popular_list)
    for movie in range(total_num):
        print '********************************'
        print str(movie) + ': \n' + '影片：'.decode('utf-8').encode('gbk') + movie_name_list[movie].decode('utf-8').encode('gbk') + '\n人气：'.decode('utf-8').encode('gbk') + movie_popular_list[movie].decode('utf-8').encode('gbk')
    input_movie_num = raw_input('\n请输入数字：'.decode('utf-8').encode('gbk'))
    print '\n影片《'.decode('utf-8').encode('gbk') + movie_name_list[int(input_movie_num)].decode('utf-8').encode('gbk') + '》 '.decode('utf-8').encode('gbk')
    detailUrl = 'http://www.dnvod.eu' + movie_address_list[int(input_movie_num)]
    # print detailUrl
    playUrl = get_play_url(detailUrl, headers)
    main(playUrl, headers)

def get_html_content(channel_url,header):
    searchRequest = urllib2.Request(channel_url,None,headers)
    searchResponse = urllib2.urlopen(searchRequest)
    searchdataResponse = searchResponse.read()
    return searchdataResponse

def regular_process(regular_str,html_con):
    #soup = BeautifulSoup(html_con,"lxml")
    #page_title = soup.title.string
    #print soup.find_all('a')
    searchReg = regular_str
    searchPattern = re.compile(searchReg)
    searchResult = searchPattern.findall(html_con)
    return searchResult

#获取ASP.NET_SessionId
def getSessionID (url2):
    try:
        s = requests.Session()
        r1 = s.get(url2)
        header = r1.headers
        rrrr = [header]
        #print rrrr[0]['Set-Cookie']
        reg = r'ASP.NET_SessionId=(.*); path=/; HttpOnly'
        partern =  re.compile(reg)
        sessionID = partern.findall(rrrr[0]['Set-Cookie'])
        return sessionID
    except urllib2.URLError,e:
        print e.code
        print e.reason


def getCookies():
    #brower = webdriver.Chrome('/Users/Junior/dev/python/chromedriver')
    brower1 = webdriver.PhantomJS(executable_path="/Users/Junior/dev/python/phantomjs-2.1.1-macosx/bin/phantomjs")
    brower1.get(url2)
    cookies = brower1.get_cookies()
    cookie = cookies[5]
    cooki = cookie["value"]
    #print cooki
    return cooki
def getUserAgent():
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36'
    return user_agent

def getHDRealUrl(urlString,low_url):
    if 'ipv6' in urlString:#判断当前网络是否走ipv6通道（因为ipv6和ipv4获得的播放网址是不一样的）
        stringOne = urlString[28:]
    else:
        stringOne = urlString[26:]
    searchVodReg = r'/(.*)/'
    searchVodPattern = re.compile(searchVodReg)
    searchVodResult = searchVodPattern.findall(stringOne)
    whichTypeVod = searchVodResult
    vodString = whichTypeVod[0]
    urlPre = urlString[:15]+'dnplayer.tv/'+vodString+'/'
    urlPreLength = len(urlPre)
    if 'ipv6' in urlString:
        urlMostimportant = urlString[urlPreLength+2:]
    else:
        urlMostimportant = urlString[urlPreLength:]
    vodList = ['vod','gvod','hvod','ivod','jvod','kvod','lvod','live']
    serverList = ['server1','server2','server3']
    try:
        urltoattend =  urlPre+urlMostimportant
        findrealRequest = urllib2.Request(urltoattend)
        findrealResponse = urllib2.urlopen(findrealRequest)
        realVIPURL = urltoattend
    except urllib2.URLError,e:
        for i in range(len(vodList)):
            urltoattend = urlString[:15] + 'dnplayer.tv/' + vodList[i] + '/' + urlMostimportant
            findrealRequest = urllib2.Request(urltoattend)
            try:
                findrealResponse = urllib2.urlopen(findrealRequest)
                realVIPURL = urltoattend
                return realVIPURL
            except urllib2.URLError, e:
                for j in range(len(serverList)):
                    urltoattend = 'http://' + serverList[j] + '.dnplayer.tv/' + vodList[i] + '/' + urlMostimportant
                    try:
                        findrealRequest = urllib2.Request(urltoattend)
                        findrealResponse = urllib2.urlopen(findrealRequest)
                        realVIPURL = urltoattend
                        return realVIPURL
                    except urllib2.HTTPError, e:
                        print "获取高清播放地址中(".decode('utf-8').encode('gbk')+str(i*3+j+1)+")...".decode('utf-8').encode('gbk')
                        realVIPURL = '无法获得高清地址，普清地址如下：\n'.decode('utf-8').encode('gbk')+low_url
    return  realVIPURL



####程序从这里开始！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！

#获取cookie，当网站出现5秒等待时，用这个方法获得cookie
#cookies = 'ASP.NET_SessionId='+getCookies()
#获取cookie，当网站未出现5秒等待时，用这个方法
cookies = 'ASP.NET_SessionId='+getSessionID(url2)[0]+";user=coF4mKWxa7hRoPjbrdbSi获得cookieK7JGOju4Ap/rTk61PVVlS1dIMx3WnCgwTTT9sR5GRp5/Y/8VhhDC4tIeqTIpgXcfRUTD0umtgDPeJCjL0XfLTDqvfjhl3RKIFhPDq1qKj5MeJ8BePXuXcaybSI2BHsQjr+gBUoddScN38wAn58q/RVe3/WzzNvtJCwx/lEZshl/lJvqIV1ynpkCUjsm"
#以上两种方式都不可以时，尝试第三种
#cookies = 'ASP.NET_SessionId=xzwrf4k0ulqctgt2boww5hk3'

#构建user agent
user_agent = getUserAgent()
#构建headers
headers = {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
"Content-Type": "application/x-www-form-urlencoded",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
"Referer": "http://www.dnvod.eu/",
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
    print '\n*****************************\n* 1,直接输入多瑙观看页面URL *\n* 2,随便看看                *\n* 3,搜索影片                *\n*****************************\n\n'.decode('utf-8')
    inputArg = raw_input('请输入数字：'.decode('utf-8').encode('gbk'))
    if inputArg == '1':
        inputurl = raw_input('\n输入多瑙观看页面URL：\n'.decode('utf-8').encode('gbk'))
        playUrl = inputurl
        main(playUrl,headers)
        loopString = False
    elif inputArg == '2':
        input_channel = raw_input('\n选择频道：\n1,电影\n2,电视剧\n3,综艺\n4,动漫\n请输入：'.decode('utf-8').encode('gbk'))
        if input_channel == '1':#电影频道
            channel_url = 'http://www.dnvod.eu/Movie/List.aspx?CID=0,1,3'
            totalNum = 55 #
            suibiankankan(channel_url,totalNum)
            loopString = False
        elif input_channel == '2':#电视剧频道
            channel_url = 'http://www.dnvod.eu/Movie/List.aspx?CID=0,1,4'
            total_num = 35  #
            suibiankankan(channel_url, total_num)
            loopString = False
        elif input_channel == '3':#综艺频道
            channel_url = 'http://www.dnvod.eu/Movie/List.aspx?CID=0,1,5'
            total_num = 35  #
            suibiankankan(channel_url, total_num)
            loopString = False
        elif input_channel == '4':#综艺频道
            channel_url = 'http://www.dnvod.eu/Movie/List.aspx?CID=0,1,6'
            total_num = 35  #
            suibiankankan(channel_url, total_num)
            loopString = False
    elif inputArg == '3':
        inputMovieName = raw_input('\n查找视频名称：'.decode('utf-8').encode('gbk'))
        if inputMovieName[0:2] == 'av':
            urlSearch = 'http://www.dnvod.eu/Adult/Search.aspx?tags='+inputMovieName[2:len(inputMovieName)]
        else:
            urlSearch = 'http://www.dnvod.eu/Movie/Search.aspx?tags='+inputMovieName
        searchdataResponse = get_html_content(urlSearch,headers)
        searchResult = regular_process(r'<a href="(.*%3d)">',searchdataResponse)
        searchResultName = regular_process(r'3d" title="(.*)">',searchdataResponse)
        #print searchResult
        print('搜索到'+str(len(searchResult))+'个结果：\n'.decode('utf-8').encode('gbk'))
        for i in range(len(searchResultName)):
            print str(i+1)+': '+searchResultName[i]+'\n'
        whichResultStr = raw_input('请输入数字：'.decode('utf-8').encode('gbk'))
        whichResultInt = int(whichResultStr)-1
        filmIdResult = regular_process(r'id=(.*%3d)',searchResult[whichResultInt])
        #print filmIdResult
        if inputMovieName[0:2] == 'av':
            searchUrl = 'http://www.dnvod.eu/Adult/detail.aspx?id='+filmIdResult[0]
        else:
            searchUrl = 'http://www.dnvod.eu/Movie/detail.aspx?id='+filmIdResult[0]
        playUrl = get_play_url(searchUrl,headers)
        print '播放页面URL：\n'.decode('utf-8')+playUrl
        main(playUrl,headers)
        loopString = False
    else:
        print '\n输入错误，请重新输入'.decode('utf-8')
