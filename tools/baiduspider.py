#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import bs4
import urllib
import urllib2
import re
import os
from multiprocessing import Pool

host = "https://shurufa.baidu.com"
archives_url = host + "/dict"

categories = []

tagsNeeded = ['全国', '上海', '重庆', '河南', '全部'] #
dicts = []

class Dict():
    def __init__(self):
        self.text = ''
        self.innerid = ''
        self.samples = ''
        self.count = ''
        self.updatedOn = ''
        self.href = ''
        self.status = ''
        pass

def loadPage(url) :
  print "loading %s ..." % (url)
  response = requests.get(url)
  print "loaded"
  return bs4.BeautifulSoup(response.content.decode("utf-8"), "html.parser")

def processCategory(cate) :
  # for cate in categories :
  cate["tags"] = []
  soup = loadPage(cate["href"])
  for tagAnchor in soup.select("div.dict-list div.tag_contain a[data-stats*='webDictListPage.category']") :
    tag = {}
    tag["text"] = tagAnchor.get_text().encode('utf-8').replace("\n", "").replace("\r", "")
    tag["href"] = host + tagAnchor.attrs["href"].encode('utf-8') + '&orderby=download'
    tag["dicts"] = [];
    cate["tags"].append(tag)
    if any(tagNeeded.find(tag["text"])>=0 for tagNeeded in tagsNeeded):
      print  '标签 %s 已识别: %s' % ( tag["text"], tag["href"] )
      processTag(tag)

def processTag(tag) :
  # for cate in categories :
  #   for tag in cate["tags"] :
  print '开始分析标签 %s ' % (tag['text'])
  soup1 = loadPage(tag["href"])
  for d in soup1.select("div.dict-list-info table tr") :
    dict1 = Dict();
    cells = d.find_all('td')
    dict1.text = cells[0].find_all('a')[0].string.encode('utf-8').replace("\n", "").replace("\r", "")
    dict1.innerid = cells[4].find_all("a")[0].attrs["dict-innerid"].encode('utf-8')
    dict1.samples = cells[1].get_text().encode('utf-8').replace("\n", "").replace("\r", "")
    dict1.count = cells[2].get_text().encode('utf-8').replace("\n", "").replace("\r", "")
    dict1.updatedOn = cells[3].get_text().encode('utf-8').replace("\n", "").replace("\r", "")
    dict1.href = host + "/dict_innerid_download?innerid=" + cells[4].find_all("a")[0].attrs["dict-innerid"].encode('utf-8')
    dict1.status = "ready"
    tag["dicts"].append(dict1)
    print "词典 %s 已识别: %s " % ( dict1.text, dict1.href )
    dicts.append(dict1)

def download_dicts():
  pool = Pool(8)
  results = pool.map(download_dict, dicts)

def download_dict(dict) :
  indexOfDict = next((i for i, item in enumerate(dicts) if item.innerid == dict.innerid), -1)
  originDict = dicts[indexOfDict]
  print '开始下载: %s (%s/%s)' % (dict.text, sum(1 for d in dicts if d.status != "ready") + 1, len(dicts))
  originDict.status = 'loading'
  if not os.path.exists('./download') :
    mkdir('./download')

  downloadFilePath = './download/%s.bdict' % (dict.innerid);
  u = urllib.urlopen(dict.href)
  data = u.read()
  f = open(downloadFilePath, 'wb')
  f.write(data)
  f.close()
  originDict.status = "loaded"
  print '下载完成: %s (%s/%s)' % (dict.text, sum(1 for d in dicts if d.status == "loaded"), len(dicts))

def mkdir(path):
    # 去除首位空格
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\")

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists=os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        print path+' 创建成功'
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print path+' 目录已存在'
        return False

def start_parse(url) :
  soup = loadPage(url)
  #soup = bs4.BeautifulSoup(response.text);

  # 为了防止漏掉调用close方法，这里使用了with语句
  # 写入到文件中的编码为utf-8
  # with open('archives.txt', 'w') as f :
  for archive in soup.select("li p.sort-title a") :
    tag = {}
    tag["text"] = archive.get_text().encode('utf-8').replace('\n', '')
    tag["href"] = host + archive.attrs["href"].encode('utf-8')
    tag["status"] = "ready"
    tag["type"] = "category"
    categories.append(tag)
    print '类别 %s 已识别' % ( tag["text"] )
    processCategory(tag)

  print "搜索完成 %s " % (len(dicts))
  download_dicts()

# 当命令行运行该模块时，__name__等于'__main__'
# 其他模块导入该模块时，__name__等于'parse_html'
if __name__ == '__main__' :
    start_parse(archives_url)
