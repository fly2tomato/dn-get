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
headers1 = {"User-Agent": user_agent,
"Host": "www.dnvod.eu",
"Cache-Control": "max-age=0",
"Upgrade-Insecure-Requests": "1",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
"DNT": "1",
"Referer": "http://www.dnvod.eu/Movie/detail.aspx?id=o0s4s2a2L%2fc%3d",
"Accept-Encoding": "",
"Accept-Language": "de-DE,de;q=0.8,en-US;q=0.6,en;q=0.4,zh-CN;q=0.2,zh;q=0.2,zh-TW;q=0.2,fr-FR;q=0.2,fr;q=0.2",
"Cookie": "__cfduid=d88efcba63bd1bdabb48eb36678b9da0d1460149942; ASP.NET_SessionId=eiwo4m450xvunmeupdmn1q45; jiathis_rdc=%7B%22http%3A//www.dnvod.eu/Movie/detail.aspx%3Fid%3D8SR7YBjBIFTNmeMectHdmg%253d%253d%22%3A1007379818%2C%22http%3A//www.dnvod.eu/Movie/detail.aspx%3Fid%3DY%252fVGTZIgb2cvsYJVGKYghA%253d%253d%22%3A1007385283%2C%22http%3A//www.dnvod.eu/Movie/Readyplay.aspx%3Fid%3Db2YL3BwS3PI%253d%22%3A1014099952%2C%22http%3A//www.dnvod.eu/Adult/detail.aspx%3Fid%3DhA1h9PheUGY%253d%22%3A1014512650%2C%22http%3A//www.dnvod.eu/Adult/detail.aspx%3Fid%3DKTbbNznK1uY%253d%22%3A1015132304%2C%22http%3A//www.dnvod.eu/Adult/Readyplay.aspx%3Fid%3DNUkPW7ehKjs%253d%22%3A1015155198%2C%22http%3A//www.dnvod.eu/Adult/detail.aspx%3Fid%3D3xCQMgLw21A%253d%22%3A1015181967%2C%22http%3A//www.dnvod.eu/Adult/detail.aspx%3Fid%3DNTKyEiVsAvY%253d%22%3A1015262975%2C%22http%3A//www.dnvod.eu/Adult/Readyplay.aspx%3Fid%3DidYsGyt8ASY%253d%22%3A1015271206%2C%22http%3A//www.dnvod.eu/Adult/detail.aspx%3Fid%3D2l1GDil1ZzA%253d%22%3A1015322087%2C%22http%3A//www.dnvod.eu/Adult/Readyplay.aspx%3Fid%3D5ZT8xTVuo1E%253d%22%3A1015325570%2C%22http%3A//www.dnvod.eu/Adult/detail.aspx%3Fid%3DKKpmTrC%252fJOA%253d%22%3A1015371926%2C%22http%3A//www.dnvod.eu/Adult/detail.aspx%3Fid%3DuQmY3qNF6ac%253d%22%3A1015386004%2C%22http%3A//www.dnvod.eu/Adult/Readyplay.aspx%3Fid%3DvDDBmW8%252blVU%253d%22%3A1015390411%2C%22http%3A//www.dnvod.eu/Adult/Readyplay.aspx%3Fid%3DwvbSBX1zKos%253d%22%3A1015409115%2C%22http%3A//www.dnvod.eu/Adult/detail.aspx%3Fid%3DHMfMaJtyOsg%253d%22%3A1015425063%2C%22http%3A//www.dnvod.eu/Adult/Readyplay.aspx%3Fid%3DNpBWcr%252bldvo%253d%22%3A1015428031%2C%22http%3A//www.dnvod.eu/Adult/detail.aspx%3Fid%3Dw9045%252fi6cxo%253d%22%3A1015494899%2C%22http%3A//www.dnvod.eu/Adult/detail.aspx%3Fid%3DZ%252bjSPbVtybA%253d%22%3A1015517309%2C%22http%3A//www.dnvod.eu/Adult/Readyplay.aspx%3Fid%3Dt8pPHpjOLZI%253d%22%3A1015521040%2C%22http%3A//www.dnvod.eu/Movie/detail.aspx%3Fid%3DN9QPrJpLpQQVBNrhQcuoHA%253d%253d%22%3A1070054703%2C%22http%3A//www.dnvod.eu/Movie/Readyplay.aspx%3Fid%3DbULYva%252bqX9M%253d%22%3A1070100585%2C%22http%3A//www.dnvod.eu/Movie/Readyplay.aspx%3Fid%3DXwOOYsSjSZM%253d%22%3A1072648110%2C%22http%3A//www.dnvod.eu/Movie/detail.aspx%3Fid%3D9Ei5yCS2poccVfR5arBRBg%253d%253d%22%3A1084764058%2C%22http%3A//www.dnvod.eu/Movie/detail.aspx%3Fid%3DjDyoiAYozqo%253d%22%3A1084845278%2C%22http%3A//www.dnvod.eu/Movie/detail.aspx%3Fid%3DUFwyU36KXsQ%253d%22%3A1084883577%2C%22http%3A//www.dnvod.eu/Movie/detail.aspx%3Fid%3DsGOV2WsoSJs%253d%22%3A1084919884%2C%22http%3A//www.dnvod.eu/Movie/Readyplay.aspx%3Fid%3DsRqcYS5kv6U%253d%22%3A1103686157%2C%22http%3A//www.dnvod.eu/Movie/Readyplay.aspx%3Fid%3DNwYqrRLZDfo%253d%22%3A1104452541%2C%22http%3A//www.dnvod.eu/Movie/detail.aspx%3Fid%3Dqs5sPkxEE9HS1o8e0m2raA%253d%253d%22%3A1104527088%2C%22http%3A//www.dnvod.eu/Movie/detail.aspx%3Fid%3Dp2c2neZcynI%253d%22%3A1105009125%2C%22http%3A//www.dnvod.eu/Movie/Readyplay.aspx%3Fid%3D%252f97CcPawDSM%253d%22%3A1105012754%2C%22http%3A//www.dnvod.eu/Movie/detail.aspx%3Fid%3DwoprA0arHp1gLT5MxNyM4Q%253d%253d%22%3A1107338005%2C%22http%3A//www.dnvod.eu/Movie/Readyplay.aspx%3Fid%3D6Lb5loU3zK4%253d%22%3A1107359089%2C%22http%3A//www.dnvod.eu/Movie/detail.aspx%3Fid%3DVu3JLUOAKOc%253d%22%3A1114137324%2C%22http%3A//www.dnvod.eu/Movie/detail.aspx%3Fid%3Dp0RKpmCFFao%253d%22%3A1114215664%2C%22http%3A//www.dnvod.eu/Movie/Readyplay.aspx%3Fid%3DDpBUkwtR4dQ%253d%22%3A1114282831%2C%22http%3A//www.dnvod.eu/Movie/detail.aspx%3Fid%3Dh3P0EzDNL3Z6kgePXHn3OA%253d%253d%22%3A1524264530%2C%22http%3A//www.dnvod.eu/Movie/Readyplay.aspx%3Fid%3DhrYE2WRziKk%253d%22%3A1524278322%2C%22http%3A//www.dnvod.eu/Movie/Readyplay.aspx%3Fid%3Dhf%252fP%252bPm5m74%253d%22%3A1525595596%2C%22http%3A//www.dnvod.eu/Movie/detail.aspx%3Fid%3DoW%252bGvQegBwMdAjvSwzF%252f1Q%253d%253d%22%3A1595212281%2C%22http%3A//www.dnvod.eu/Movie/Readyplay.aspx%3Fid%3Dw1B1Bklk4aI%253d%22%3A1595215089%2C%22http%3A//www.dnvod.eu/Movie/Readyplay.aspx%3Fid%3DNkxO8WQPOAE%253d%22%3A1597941260%2C%22http%3A//www.dnvod.eu/Movie/Readyplay.aspx%3Fid%3DMWgGa5UahNE%253d%22%3A%220%7C1466184905815%22%7D; dn_config=device=desktop&player=CkPlayer; autologin=username=fly2tomato&userpwd=GMK1munp; user=JTUcjSxTLZyf8dxO9NjtTTYZxPSz_neZdKYP0J6JTDgUBF6Ky_seKld5ACOrgu7TMrd674GPKQ5Bp9TAiw4erxaOVV1jCTazcFG_cf6p0pNGToMtAzAgI81XiuO8WaGmYkMrWeaih24ERrvzagNaT1FlFT604-kC9kEl5k5io5CuWOpo-jJJn5QgFFq_nDS3DW_2aXAKWj_nNcGnHtsWX0D9r5L3NBN9uRNQAMVvYKduZvS1FBgxTBwTH7ct4nUm7bbLiw2; _ga=GA1.2.1028940840.1460149947; _uid=2f6eb3fafcb6412f862e0cbb49d2ab43"}
headers2 = {"User-Agent": user_agent,
"Host": "www.dnvod.eu",
"Content-Length": "36",
"Origin": "http://www.dnvod.eu",
"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
"Accept": "*/*",
"Referer": "http://www.dnvod.eu/Movie/Readyplay.aspx?id=GnPAXV40la4%3d",
"Accept-Encoding": "gzip, deflate",
"Accept-Language": "de-DE,de;q=0.8,en-US;q=0.6,en;q=0.4,zh-CN;q=0.2,zh;q=0.2,zh-TW;q=0.2,fr-FR;q=0.2,fr;q=0.2",
"X-Requested-With": "XMLHttpRequest",
"DNT": "1",
"Cache-Control": "max-age=0",
"Connection": "keep-alive",
"Cookie": "__cfduid=d88efcba63bd1bdabb48eb36678b9da0d1460149942; ASP.NET_SessionId=eiwo4m450xvunmeupdmn1q45; jiathis_rdc=%7B%22http%3A//www.dnvod.eu/Movie/detail.aspx%3Fid%3D8SR7YBjBIFTNmeMectHdmg%253d%253d%22%3A1007379818%2C%22http%3A//www.dnvod.eu/Movie/detail.aspx%3Fid%3DY%252fVGTZIgb2cvsYJVGKYghA%253d%253d%22%3A1007385283%2C%22http%3A//www.dnvod.eu/Movie/Readyplay.aspx%3Fid%3Db2YL3BwS3PI%253d%22%3A1014099952%2C%22http%3A//www.dnvod.eu/Adult/detail.aspx%3Fid%3DhA1h9PheUGY%253d%22%3A1014512650%2C%22http%3A//www.dnvod.eu/Adult/detail.aspx%3Fid%3DKTbbNznK1uY%253d%22%3A1015132304%2C%22http%3A//www.dnvod.eu/Adult/Readyplay.aspx%3Fid%3DNUkPW7ehKjs%253d%22%3A1015155198%2C%22http%3A//www.dnvod.eu/Adult/detail.aspx%3Fid%3D3xCQMgLw21A%253d%22%3A1015181967%2C%22http%3A//www.dnvod.eu/Adult/detail.aspx%3Fid%3DNTKyEiVsAvY%253d%22%3A1015262975%2C%22http%3A//www.dnvod.eu/Adult/Readyplay.aspx%3Fid%3DidYsGyt8ASY%253d%22%3A1015271206%2C%22http%3A//www.dnvod.eu/Adult/detail.aspx%3Fid%3D2l1GDil1ZzA%253d%22%3A1015322087%2C%22http%3A//www.dnvod.eu/Adult/Readyplay.aspx%3Fid%3D5ZT8xTVuo1E%253d%22%3A1015325570%2C%22http%3A//www.dnvod.eu/Adult/detail.aspx%3Fid%3DKKpmTrC%252fJOA%253d%22%3A1015371926%2C%22http%3A//www.dnvod.eu/Adult/detail.aspx%3Fid%3DuQmY3qNF6ac%253d%22%3A1015386004%2C%22http%3A//www.dnvod.eu/Adult/Readyplay.aspx%3Fid%3DvDDBmW8%252blVU%253d%22%3A1015390411%2C%22http%3A//www.dnvod.eu/Adult/Readyplay.aspx%3Fid%3DwvbSBX1zKos%253d%22%3A1015409115%2C%22http%3A//www.dnvod.eu/Adult/detail.aspx%3Fid%3DHMfMaJtyOsg%253d%22%3A1015425063%2C%22http%3A//www.dnvod.eu/Adult/Readyplay.aspx%3Fid%3DNpBWcr%252bldvo%253d%22%3A1015428031%2C%22http%3A//www.dnvod.eu/Adult/detail.aspx%3Fid%3Dw9045%252fi6cxo%253d%22%3A1015494899%2C%22http%3A//www.dnvod.eu/Adult/detail.aspx%3Fid%3DZ%252bjSPbVtybA%253d%22%3A1015517309%2C%22http%3A//www.dnvod.eu/Adult/Readyplay.aspx%3Fid%3Dt8pPHpjOLZI%253d%22%3A1015521040%2C%22http%3A//www.dnvod.eu/Movie/detail.aspx%3Fid%3DN9QPrJpLpQQVBNrhQcuoHA%253d%253d%22%3A1070054703%2C%22http%3A//www.dnvod.eu/Movie/Readyplay.aspx%3Fid%3DbULYva%252bqX9M%253d%22%3A1070100585%2C%22http%3A//www.dnvod.eu/Movie/Readyplay.aspx%3Fid%3DXwOOYsSjSZM%253d%22%3A1072648110%2C%22http%3A//www.dnvod.eu/Movie/detail.aspx%3Fid%3D9Ei5yCS2poccVfR5arBRBg%253d%253d%22%3A1084764058%2C%22http%3A//www.dnvod.eu/Movie/detail.aspx%3Fid%3DjDyoiAYozqo%253d%22%3A1084845278%2C%22http%3A//www.dnvod.eu/Movie/detail.aspx%3Fid%3DUFwyU36KXsQ%253d%22%3A1084883577%2C%22http%3A//www.dnvod.eu/Movie/detail.aspx%3Fid%3DsGOV2WsoSJs%253d%22%3A1084919884%2C%22http%3A//www.dnvod.eu/Movie/Readyplay.aspx%3Fid%3DsRqcYS5kv6U%253d%22%3A1103686157%2C%22http%3A//www.dnvod.eu/Movie/Readyplay.aspx%3Fid%3DNwYqrRLZDfo%253d%22%3A1104452541%2C%22http%3A//www.dnvod.eu/Movie/detail.aspx%3Fid%3Dqs5sPkxEE9HS1o8e0m2raA%253d%253d%22%3A1104527088%2C%22http%3A//www.dnvod.eu/Movie/detail.aspx%3Fid%3Dp2c2neZcynI%253d%22%3A1105009125%2C%22http%3A//www.dnvod.eu/Movie/Readyplay.aspx%3Fid%3D%252f97CcPawDSM%253d%22%3A1105012754%2C%22http%3A//www.dnvod.eu/Movie/detail.aspx%3Fid%3DwoprA0arHp1gLT5MxNyM4Q%253d%253d%22%3A1107338005%2C%22http%3A//www.dnvod.eu/Movie/Readyplay.aspx%3Fid%3D6Lb5loU3zK4%253d%22%3A1107359089%2C%22http%3A//www.dnvod.eu/Movie/detail.aspx%3Fid%3DVu3JLUOAKOc%253d%22%3A1114137324%2C%22http%3A//www.dnvod.eu/Movie/detail.aspx%3Fid%3Dp0RKpmCFFao%253d%22%3A1114215664%2C%22http%3A//www.dnvod.eu/Movie/Readyplay.aspx%3Fid%3DDpBUkwtR4dQ%253d%22%3A1114282831%2C%22http%3A//www.dnvod.eu/Movie/detail.aspx%3Fid%3Dh3P0EzDNL3Z6kgePXHn3OA%253d%253d%22%3A1524264530%2C%22http%3A//www.dnvod.eu/Movie/Readyplay.aspx%3Fid%3DhrYE2WRziKk%253d%22%3A1524278322%2C%22http%3A//www.dnvod.eu/Movie/Readyplay.aspx%3Fid%3Dhf%252fP%252bPm5m74%253d%22%3A1525595596%2C%22http%3A//www.dnvod.eu/Movie/detail.aspx%3Fid%3DoW%252bGvQegBwMdAjvSwzF%252f1Q%253d%253d%22%3A1595212281%2C%22http%3A//www.dnvod.eu/Movie/Readyplay.aspx%3Fid%3Dw1B1Bklk4aI%253d%22%3A1595215089%2C%22http%3A//www.dnvod.eu/Movie/Readyplay.aspx%3Fid%3DNkxO8WQPOAE%253d%22%3A1597941260%2C%22http%3A//www.dnvod.eu/Movie/Readyplay.aspx%3Fid%3DMWgGa5UahNE%253d%22%3A%220%7C1466184905815%22%7D; dn_config=device=desktop&player=CkPlayer; autologin=username=fly2tomato&userpwd=GMK1munp; user=JTUcjSxTLZyf8dxO9NjtTTYZxPSz_neZdKYP0J6JTDgUBF6Ky_seKld5ACOrgu7TMrd674GPKQ5Bp9TAiw4erxaOVV1jCTazcFG_cf6p0pNGToMtAzAgI81XiuO8WaGmYkMrWeaih24ERrvzagNaT1FlFT604-kC9kEl5k5io5CuWOpo-jJJn5QgFFq_nDS3DW_2aXAKWj_nNcGnHtsWX0D9r5L3NBN9uRNQAMVvYKduZvS1FBgxTBwTH7ct4nUm7bbLiw2; _ga=GA1.2.1028940840.1460149947; _uid=2f6eb3fafcb6412f862e0cbb49d2ab43"}

inputurl = raw_input('输入多瑙观看页面URL：\n')
urlFir = inputurl
requestFir = urllib2.Request(urlFir,None,headers1)
responseFir  = urllib2.urlopen(requestFir)
data_responseFir = responseFir.read()
print data_responseFir

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
print para1
if cmp(para1,"Adult") == 0:
    start_id = index_id_String+4
else:
    start_id = index_id_String+5
end_id = index_3d_String+3
filttedstring = tobefilttedstring[start_id:end_id]#获得id
print filttedstring
print para1
para2 = filttedstring#id

urlSec = 'http://www.dnvod.eu/'+para1+'/GetResource.ashx?id='+para2+'&type=htm'

requestSec = urllib2.Request(urlSec,None,headers2)
responseSec = urllib2.urlopen(requestSec)
real_url = responseSec.read()
print "\n~~~~~~~~播放地址（直接复制到浏览器打开或者用迅雷下载）：~~~~~~~~\n"
if cmp(para1,"Adult") == 0:
    pattern0 = re.compile(r'(\d||\d\d)\.mp4')
    num0 = re.split(pattern0,real_url)
    hdurl = num0[0]+'1'+'.mp4'+num0[2]
    print '预览版: \n'+real_url
    print '完整版: \n'+hdurl
else:
    print "低清版: \n"+real_url
    pattern = re.compile(r'(\d||\d\d||\d\d\d||\d\d\d\d||\d\d\d\d\d||\d\d\d\d\d\d||\d\d\d\d\d\d\d||\d\d\d\d\d\d\d\d)\.mp4')
    num = re.split(pattern,real_url)
    hdurl = num[0]+'hd-'+num[1]+'.mp4'+num[2]
    print "高清版: \n"+hdurl
