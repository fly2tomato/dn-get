by fly2tomato

# issues

  返回“-3”？ 表示key不对  
  返回“-4”？ ASP.NET_SessionId已过期需要重新获取


# update

 【29.07.2016】增加了高清片源url  
 【01.08.2016】自动获取ASP.NET_SessionId（该值是否作为cookie中唯一判断标准，待检验）

# 实现功能：

  1，获得多瑙真实播放地址，该地址可直接在浏览器中播放或者用下载工具（迅雷，you-get等）下载，屏蔽广告

  2，大福利：免费看多瑙vipAV

# 使用方法：

  1，浏览器登录多瑙，进入影片播放页面，将播放页面的url复制，

  2，然后在shell运行： python dn—get.py； 回车

  3，输入复制的url，回车

  4，获得真实播放地址，command+点击播放地址，直接调用默认浏览器开始播放
