# 亲爱的们，教程比较旧了，百度贴吧页面可能改版，可能代码不好使，八成是正则表达式那儿匹配不到了，请更改一下正则，当然最主要的还是帮助大家理解思路。
# 2016/12/2

# 本篇目标
# 1.对百度贴吧的任意帖子进行抓取
# 2.指定是否只抓取楼主发帖内容
# 3.将抓取到的内容分析并保存到文件
__author__ = 'CQC'
# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
 
#百度贴吧爬虫类
class BDTB:
    #初始化，传入基地址，是否只看楼主的参数
    def __init__(self, baseUrl, seeLZ):
        self.baseURL = baseUrl
        self.seeLZ = '?see_lz='+str(seeLZ)
 
    #传入页码，获取该页帖子的代码
    def getPage(self, pageNum):
        try:
            url = self.baseURL + self.seeLZ + '&pn=' + str(pageNum)
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            print response.read()
            return response
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"连接百度贴吧失败,错误原因",e.reason
                return None
 

baseURL = 'http://tieba.baidu.com/p/3138733512'
bdtb = BDTB(baseURL, 1)
bdtb.getPage(1)