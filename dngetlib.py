# !/usr/bin/env python
#-*-coding:utf-8-*-
#by fly2tomato
import urllib
import urllib2
import re
import requests
import os


user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
#获取cookie，当网站出现5秒等待时，用这个方法获得cookie
#cookies = 'ASP.NET_SessionId='+getCookies()
#获取cookie，当网站未出现5秒等待时，用这个方法
#cookies = 'ASP.NET_SessionId='+getSessionID(url2)[0]+";user=coF4mKWxa7hRoPjbrdbSi获得cookieK7JGOju4Ap/rTk61PVVlS1dIMx3WnCgwTTT9sR5GRp5/Y/8VhhDC4tIeqTIpgXcfRUTD0umtgDPeJCjL0XfLTDqvfjhl3RKIFhPDq1qKj5MeJ8BePXuXcaybSI2BHsQjr+gBUoddScN38wAn58q/RVe3/WzzNvtJCwx/lEZshl/lJvqIV1ynpkCUjsm"
#以上两种方式都不可以时，尝试第三种
cookies = 'ASP.NET_SessionId=xzwrf4k0ulqctgt2boww5hk3'
#构建user agent
#user_agent = getUserAgent()
#构建headers
headers = {"User-Agent": user_agent,
"Content-Type": "application/x-www-form-urlencoded",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
"Referer": "http://www.dnvod.eu/",
#"Content-Length": "36",
"Accept-Encoding": "",
"Accept-Language": "de-DE,de;q=0.8,en-US;q=0.6,en;q=0.4,zh-CN;q=0.2,zh;q=0.2,zh-TW;q=0.2,fr-FR;q=0.2,fr;q=0.2",
"X-Requested-With": "XMLHttpRequest",
"DNT": "1",
"Cookie": cookies}

def dnget(playUrl):
    real_url = get_real_url(playUrl)
    #print real_url
    data_responseFir = get_html_content(playUrl)
    para1 = playUrl[20:25]#Adult or Movie
    #print para1
    para2 = regular_process(r'id:.*\'(.*)\',',data_responseFir)[0]
    #print "\nID:                 "+para2
    #print '\nKey:                '+keyString
    #print '\nASP.NET_SessionId:  '+sessionID
    if real_url == "-4":
        print 'ASP.NET_SessionID已过期，请重新获取'
        hdurl = 'ASP.NET_SessionID已过期，请重新获取'
    elif real_url == "-3":
        print 'key错误，请重新设置key'
        hdurl = 'key错误，请重新设置key'
    else:
        hdurl = hdurl_print(real_url,para1,para2)
    return hdurl

def hdurl_print(real_url,para1,para2):
    print "\n********真实播放地址（直接复制到浏览器打开或者用工具下载）：********\n"
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
        #print "低清版: \n"+real_url+'\n'
        hdurl0 = num[0] + 'hd-' + num[1] + '.mp4' + num[2]
        hdurl = getHDRealUrl(hdurl0,real_url)
        print " 高清版: \n"+hdurl+'\n'
    return hdurl

def get_real_url(playUrl):
    data_responseFir = get_html_content(playUrl)
    para1 = playUrl[20:25]#Adult or Movie
    para2 = regular_process(r'id:.*\'(.*)\',',data_responseFir)[0]
    urlSec = 'http://www.dnvod.eu/'+para1+'/GetResource.ashx?id='+para2+'&type=htm'
    keyString = regular_process(r'key:.*\'(.*)\',',data_responseFir)[0]
    data = urllib.urlencode({'key':keyString})
    requestSec = urllib2.Request(urlSec,data,headers)
    responseSec = urllib2.urlopen(requestSec)
    real_url = responseSec.read()
    real_url = regular_process(r'<>(.*)<>',real_url)[0]
    return real_url

def get_play_url(searchUrl):
    detail_content = get_html_content(searchUrl)
    episode_list = regular_process(r'Readyplay.aspx\?id=(.*)" target',detail_content)
    totalEps = len(episode_list)
    #print detailResult
    whichEpisodeStr = raw_input("一共有"+str(totalEps)+"集，请选择集数：")
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


def get_html_content(channel_url):
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
    if 'ipv6' in urlString:  # 判断当前网络是否走ipv6通道（因为ipv6和ipv4获得的播放网址是不一样的）
        stringOne = urlString[26:36]
    else:
        stringOne = urlString[24:34]
    searchVodReg = r'/(.*)/'
    searchVodPattern = re.compile(searchVodReg)
    searchVodResult = searchVodPattern.findall(stringOne)
    whichTypeVod = searchVodResult
    vodString = whichTypeVod[0]
    urlPre = urlString[:15] + 'dnplayer.tv/' + vodString + '/'
    urlPreLength = len(urlPre)
    if 'ipv6' in urlString:
        urlMostimportant = urlString[urlPreLength + 2:]
    else:
        urlMostimportant = urlString[urlPreLength:]
    vodList = ['vod', 'gvod', 'hvod', 'ivod', 'jvod', 'kvod', 'lvod', 'live']
    # serverList = ['server1', 'server2', 'server3']
    serverList = ['server1', 'server2', 'server3', 'server4', 'server5', 'server6']
    try:
        urltoattend = urlPre + urlMostimportant
        findrealRequest = urllib2.Request(urltoattend)
        findrealResponse = urllib2.urlopen(findrealRequest)
        realVIPURL = urltoattend
    except urllib2.URLError, e:
        for i in range(len(vodList)):
            urltoattend = urlString[:15] + 'dnplayer.tv/' + vodList[i] + '/' + urlMostimportant
            findrealRequest = urllib2.Request(urltoattend)
            # print urltoattend
            try:
                findrealResponse = urllib2.urlopen(findrealRequest)
                realVIPURL = urltoattend
                return realVIPURL
            except urllib2.URLError, e:
                for j in range(len(serverList)):
                    urltoattend = 'http://' + serverList[j] + '.dnplayer.tv/' + vodList[i] + '/' + urlMostimportant
                    # print urltoattend
                    try:
                        findrealRequest = urllib2.Request(urltoattend)
                        findrealResponse = urllib2.urlopen(findrealRequest)
                        realVIPURL = urltoattend
                        return realVIPURL
                    except urllib2.HTTPError, e:
                        print "获取高清播放地址中(" + str(i * 6 + j + 1) + ")..."
                        realVIPURL = '无法获得高清地址，普清地址如下：\n' + low_url
    return realVIPURL

def suibiankankan(channel_url,total_num):
    html_content = get_html_content(channel_url)
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
        print str(movie) + ': \n' + '影片：' + movie_name_list[movie] + '\n人气：' + movie_popular_list[movie]
    input_movie_num = raw_input('\n请输入数字：')
    print '\n影片《' + movie_name_list[int(input_movie_num)] + '》 '
    detailUrl = 'http://www.dnvod.eu' + movie_address_list[int(input_movie_num)]
    # print detailUrl
    playUrl = get_play_url(detailUrl)
    dnget(playUrl)


def main():
    pass

if __name__ == '__main__':
    main()
