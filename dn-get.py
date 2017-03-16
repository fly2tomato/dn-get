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
import urllib2
import re
import requests
import os

import dngetlib


url1 = 'http://www.dnvod.eu/'
url2 = 'http://www.dnvod.eu/Movie/Readyplay.aspx?id=9Qm2PeBpd5s%3d'

def dn(playUrl,headers):
    real_url = dngetlib.get_real_url(playUrl)
    #print real_url
    data_responseFir = dngetlib.get_html_content(playUrl)
    para1 = playUrl[20:25]#Adult or Movie
    #print para1
    para2 = dngetlib.regular_process(r'id:.*\'(.*)\',',data_responseFir)[0]
    #print "\nID:                 "+para2
    #print '\nKey:                '+keyString
    #print '\nASP.NET_SessionId:  '+sessionID
    if real_url == "-4":
        print 'ASP.NET_SessionID已过期，请重新获取'
    elif real_url == "-3":
        print 'key错误，请重新设置key'
    else:
        hdurl = dngetlib.hdurl_print(real_url,para1,para2)
    bDownload = raw_input('\n是否需要下载视频到当前目录(for mac and linux only)？(y/n)')
    if bDownload == 'y':
        os.system('axel -a -n 5 '+hdurl)
    else:
        isPlay = raw_input('\n是否需要在线播放该视频(for mac and linux only)？(y/n)')
        if isPlay == 'y':
            os.system('mplayer '+hdurl)
        else:
            print '\nlove & peace\nfly2tomato\n'

def main():
    loopString = True
    while(loopString):
        inputArg = raw_input('\n*****************************\n* 1,直接输入多瑙观看页面URL *\n* 2,随便看看                *\n* 3,搜索影片                *\n*****************************\n\n请输入数字：')
        if inputArg == '1':
            inputurl = raw_input('\n输入多瑙观看页面URL：\n')
            playUrl = inputurl
            dngetlib.dnget(playUrl)
            loopString = False
        elif inputArg == '2':
            input_channel = raw_input('\n选择频道：\n1,电影\n2,电视剧\n3,综艺\n4,动漫\n请输入：')
            if input_channel == '1':#电影频道
                channel_url = 'http://www.dnvod.eu/Movie/List.aspx?CID=0,1,3'
                totalNum = 55 #
                dngetlib.suibiankankan(channel_url,totalNum)
                loopString = False
            elif input_channel == '2':#电视剧频道
                channel_url = 'http://www.dnvod.eu/Movie/List.aspx?CID=0,1,4'
                total_num = 35  #
                dngetlib.suibiankankan(channel_url, total_num)
                loopString = False
            elif input_channel == '3':#综艺频道
                channel_url = 'http://www.dnvod.eu/Movie/List.aspx?CID=0,1,5'
                total_num = 35  #
                dngetlib.suibiankankan(channel_url, total_num)
                loopString = False
            elif input_channel == '4':#综艺频道
                channel_url = 'http://www.dnvod.eu/Movie/List.aspx?CID=0,1,6'
                total_num = 35  #
                dngetlib.suibiankankan(channel_url, total_num)
                loopString = False
        elif inputArg == '3':
            inputMovieName = raw_input('\n查找视频名称：')
            if inputMovieName[0:2] == 'av':
                urlSearch = 'http://www.dnvod.eu/Adult/Search.aspx?tags='+inputMovieName[2:len(inputMovieName)]
            else:
                urlSearch = 'http://www.dnvod.eu/Movie/Search.aspx?tags='+inputMovieName
            searchdataResponse = dngetlib.get_html_content(urlSearch)
            searchResult = dngetlib.regular_process(r'<a href="(.*%3d)">',searchdataResponse)
            searchResultName = dngetlib.regular_process(r'3d" title="(.*)">',searchdataResponse)
            #print searchResult
            print('搜索到'+str(len(searchResult))+'个结果：\n')
            for i in range(len(searchResultName)):
                print str(i+1)+': '+searchResultName[i]+'\n'
            whichResultStr = raw_input('请输入数字：')
            whichResultInt = int(whichResultStr)-1
            filmIdResult = dngetlib.regular_process(r'id=(.*%3d)',searchResult[whichResultInt])
            #print filmIdResult
            if inputMovieName[0:2] == 'av':
                searchUrl = 'http://www.dnvod.eu/Adult/detail.aspx?id='+filmIdResult[0]
            else:
                searchUrl = 'http://www.dnvod.eu/Movie/detail.aspx?id='+filmIdResult[0]
            playUrl = dngetlib.get_play_url(searchUrl)
            print '播放页面URL：\n'+playUrl
            dngetlib.dnget(playUrl)
            loopString = False
        else:
            print '\n输入错误，请重新输入'


####程序从这里开始！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
if __name__ == '__main__':
    main()
    
