# -*- coding:utf-8 -*-
import urllib
import urllib2


# page = 1
# url = 'http://www.qiushibaike.com/hot/page/' + str(page)
# try:
#     request = urllib2.Request(url)
#     response = urllib2.urlopen(request)
#     print response.read()
# except urllib2.URLError, e:
#     if hasattr(e,"code"):
#         print e.code
#     if hasattr(e,"reason"):
#         print e.reason

page = 1
url = 'http://www.qiushibaike.com/hot/page/' + str(page)
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = { 'User-Agent' : user_agent }
try:
    request = urllib2.Request(url,headers = headers)
    response = urllib2.urlopen(request)
    # print response.read()
    content = response.read().decode('utf-8')
    ###每一个段子都是<div class=”article block untagged mb15″ id=”…”>…</div>包裹的内容
    ###现在我们想获取发布人，发布日期，段子内容，以及点赞的个数。不过另外注意的是，段子有些是带图片的，如果我们想在控制台显示图片是不现实的，所以我们直接把带有图片的段子给它剔除掉，只保存仅含文本的段子。
    pattern = re.compile('<div.*?author">.*?<a.*?<img.*?>(.*?)</a>.*?<div.*?'+
                            'content">(.*?)<!--(.*?)-->.*?</div>(.*?)<div class="stats.*?class="number">(.*?)</i>',re.S)
    items = re.findall(pattern,content)#re.findall 是找寻所有匹配的内容
    # for item in items:
    #     print item[0],item[1],item[2],item[3],item[4]
    for item in items:
        haveImg = re.search("img",item[3])
        if not haveImg:
            print item[0],item[1],item[2],item[4]
except urllib2.URLError, e:
    if hasattr(e,"code"):
        print e.code
    if hasattr(e,"reason"):
        print e.reason

"""
现在正则表达式在这里稍作说明
1）.*? 是一个固定的搭配，.和*代表可以匹配任意无限多个字符，加上？表示使用非贪婪模式进行匹配，也就是我们会尽可能短地做匹配，以后我们还会大量用到 .*? 的搭配。
2）(.*?)代表一个分组，在这个正则表达式中我们匹配了五个分组，在后面的遍历item中，item[0]就代表第一个(.*?)所指代的内容，item[1]就代表第二个(.*?)所指代的内容，以此类推。
3）re.S 标志代表在匹配时为点任意匹配模式，点 . 也可以代表换行符。
这样我们就获取了发布人，发布时间，发布内容，附加图片以及点赞数。

在这里注意一下，我们要获取的内容如果是带有图片，直接输出出来比较繁琐，所以这里我们只获取不带图片的段子就好了。
所以，在这里我们就需要对带图片的段子进行过滤。
我们可以发现，带有图片的段子会带有类似下面的代码，而不带图片的则没有，所以，我们的正则表达式的item[3]就是获取了下面的内容，如果不带图片，item[3]获取的内容便是空。
<div class="thumb">
 
<a href="/article/112061287?list=hot&amp;s=4794990" target="_blank">
<img src="http://pic.qiushibaike.com/system/pictures/11206/112061287/medium/app112061287.jpg" alt="但他们依然乐观">
</a>
 
</div>
"""