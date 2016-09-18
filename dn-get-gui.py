#!/usr/bin/python
# -*- coding: UTF-8 -*-

from Tkinter import *
import urllib
import httplib
import urllib2
import re
import requests
import os
import sys

class dnget:
    def __init__(self):

        choice = 0
        searchResult = ''

        window = Tk() # 创建一个窗口
        window.title('多瑙影院影片搜索小工具v0.1') # 设置标题



        frame1 = Frame(window) # 创建一个框架
        frame1.pack() # 将框架frame1放置在window中



        self.v2 = IntVar()
        # 创建两个单选按钮，放置在frame1中，按钮文本是分别是Red和Yellow，背景色分别是红色和黄色，
        # 当rbRed按钮被选中时self.v2为1,当rbYellow按钮被选中时，self.v2为2，按钮被点击时触发processRadiobutto函数
        rbSearch = Radiobutton(frame1,text='搜索影片',bg='red',variable=self.v2,value=1,command=self.processRadiobutton)
        rbURL = Radiobutton(frame1,text="直接输入多瑙观看页面URL",bg="yellow",variable=self.v2,value=2,command=self.processRadiobutton)

        # grid布局
        rbSearch.grid(row=1,column=1)
        rbURL.grid(row=1,column=2)


        frame2 = Frame(window)   # 创建框架fram0e2
        frame2.pack()            # 将frame2放置在window中

        label = Label(frame2,text="请输入: ")   # 创建标签
        self.name = StringVar()
        # 创建Entry，内容是与self.name关联
        entryName = Entry(frame2, textvariable=self.name)
        # 创建按钮，点击按钮时触发processButton函数
        btGetName = Button(frame2,text="运行", command=self.processButton1)





        # grid布局
        label.grid(row=1,column=1)
        entryName.grid(row=1,column=2)
        btGetName.grid(row=1,column=3)

        # 创建格式化文本，并放置在window中
        text = Text(window)
        text.pack()
        text.insert(END,'TIP')
        text.insert(END,searchResult)


        # 监测事件直到window被关闭
        window.mainloop()

    # 单选按钮点击函数
    def processRadiobutton(self):
        global choice
        if self.v2.get() == 1:
            choice = 1
        else:
            choice = 2
        print (("搜索影片" if self.v2.get() == 1 else "直接输入多瑙观看页面URL")
               + " is selected.\n choice is "+str(choice))


    # Get Name按钮点击函数
    def processButton1(self):
        if self.name.get()[0:2] == 'av':
            urlSearch = 'http://www.dnvod.eu/Adult/Search.aspx?tags='+self.name.get()[2:len(self.name.get())]
            searchRequest = urllib2.Request(urlSearch,None,headers)
            searchResponse = urllib2.urlopen(searchRequest)
            searchdataResponse = searchResponse.read()
            #print searchdataResponse
            searchReg = r'<a href="(.*%3d)">'
        else:
            urlSearch = 'http://www.dnvod.eu/Movie/Search.aspx?tags='+self.name.get()
            searchRequest = urllib2.Request(urlSearch,None,headers)
            searchResponse = urllib2.urlopen(searchRequest)
            searchdataResponse = searchResponse.read()
            #print searchdataResponse
            searchReg = r'<a href="/\w(.*%3d)">'
        searchPattern = re.compile(searchReg)
        global searchResult
        searchResult = searchPattern.findall(searchdataResponse)
        searchRegName = r'3d" title="(.*)">'
        searchPatternName = re.compile(searchRegName)
        searchResultName = searchPatternName.findall(searchdataResponse)
        print searchResult
        print('搜索到'+str(len(searchResult))+'个结果：\n')
        for i in range(len(searchResultName)):
            print str(i+1)+': '+searchResultName[i]+'\n'

        whichResultStr = raw_input('请输入数字：')
        whichResultInt = int(whichResultStr)-1

        if self.name.get()[0:2] == 'av':
    	    searchUrl = 'http://www.dnvod.eu/Adult/'+searchResult[whichResultInt]
        else:
    	    searchUrl = 'http://www.dnvod.eu/M'+searchResult[whichResultInt]

        print searchResult[whichResultInt]
        print searchUrl
        detailRequest = urllib2.Request(searchUrl,None,headers)
        detailResponse = urllib2.urlopen(detailRequest)
        detaildataResponse = detailResponse.read()
        detailReg = r'<li><div class="bfan-n.*"><a href="(.*)" target="_blank">.*</a></div></li>'
        detailPattern = re.compile(detailReg)
        detailResult = detailPattern.findall(detaildataResponse)
        whichEpisodeStr = raw_input("一共有"+str(len(detailResult))+"集，请选择集数：")
        whichEpisodeInt = int(whichEpisodeStr)-1
        if self.name.get()[0:2] == 'av':
            playUrl = 'http://www.dnvod.eu/Adult/'+detailResult[whichEpisodeInt]
        else:
    	    playUrl = 'http://www.dnvod.eu'+detailResult[whichEpisodeInt]
        print '播放页面URL：\n'+playUrl

    # Get Name按钮点击函数
    def processButton2(self):
        playUrl = self.name.get()
        searchPattern = re.compile(searchReg)
        global searchResult
        searchResult = searchPattern.findall(searchdataResponse)
        searchRegName = r'3d" title="(.*)">'
        searchPatternName = re.compile(searchRegName)
        searchResultName = searchPatternName.findall(searchdataResponse)
        print searchResult
        print('搜索到'+str(len(searchResult))+'个结果：\n')



#获取ASP.NET_SessionId
def getSessionID (url1,url2):
    s=requests.Session()
    s.get(url1)
    r1 = s.get(url2)
    header = r1.headers
    rrrr = [header]
    #print rrrr[0]['Set-Cookie']
    reg = r'ASP.NET_SessionId=(.*); path=/; HttpOnly'
    partern =  re.compile(reg)
    sessionID = partern.findall(rrrr[0]['Set-Cookie'])
    return sessionID
def getCookies():
    cookies = 'ASP.NET_SessionId='+sessionID
    return cookies
def getUserAgent():
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    return user_agent

#宏定义
url1 = 'http://www.dnvod.eu'
url2 = 'http://www.dnvod.eu/Movie/Readyplay.aspx?id=7COqHhPaRZg%3d'
sessionID = getSessionID(url1,url2)[0]
cookies = getCookies()
user_agent = getUserAgent()
#构建headers
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

#入口

dnget()
