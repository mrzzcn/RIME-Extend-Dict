#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import bs4
import urllib.request
import os
from multiprocessing import Pool
from pypinyin import pinyin, Style

host = "https://shurufa.baidu.com"
archives_url = host + "/dict"
downloadPath = './download'
debug = []
categories = []

dicts = []


class Dict():
    def __init__(self):
        self.directory = ''
        self.text = ''
        self.innerId = ''
        self.samples = ''
        self.count = ''
        self.updatedOn = ''
        self.href = ''
        self.status = ''

    pass


def loadPage(url):
    print("loading %s ..." % url)
    response = requests.get(url)
    print("loaded")
    return bs4.BeautifulSoup(response.content.decode("utf-8"), "html.parser")


def processCategory(cate):
    # for cate in categories :
    cate["tags"] = []
    print('开始处理 %s' % cate['text'])
    soup = loadPage(cate["href"])
    subCategories = soup.select("div.dict-list div.tag_contain a[data-stats*='webDictListPage.category']")
    print('找到 %s 个二级分类' % len(subCategories))
    for tagAnchor in subCategories:
        tag = {
            "category": cate,
            "text": str(tagAnchor.get_text()).replace("\n", "").replace("\r", ""),
            "href": host + tagAnchor.attrs["href"] + '&orderby=download',
            "dicts": []
        }
        cate["tags"].append(tag)
        print('已识别标签 %s: %s' % (tag["text"], tag["href"]))
        processTag(tag)


def processTag(tag):
    # for cate in categories :
    #   for tag in cate["tags"] :
    print('开始分析标签 %s ' % tag['text'])
    soup1 = loadPage(tag["href"])
    for d in soup1.select("div.dict-list-info table tr"):
        dict1 = Dict()
        cells = d.find_all('td')
        dict1.directory = tag['category']['pinyin']
        dict1.text = str(cells[0].find_all('a')[0].string).replace("\n", "").replace("\r", "")
        dict1.innerId = cells[4].find_all("a")[0].attrs["dict-innerid"]
        dict1.samples = str(cells[1].get_text()).replace("\n", "").replace("\r", "")
        dict1.count = str(cells[2].get_text()).replace("\n", "").replace("\r", "")
        dict1.updatedOn = str(cells[3].get_text()).replace("\n", "").replace("\r", "")
        dict1.href = host + "/dict_innerid_download?innerid=" + str(cells[4].find_all("a")[0].attrs["dict-innerid"])
        dict1.status = "ready"
        tag["dicts"].append(dict1)
        print("已识别词典 %s: %s " % (dict1.text, dict1.href))
        dicts.append(dict1)


def download_dicts():
    pool = Pool(8)
    total = len(dicts)
    results = pool.map(download_dict, dicts, 1)
    pool.close()


def download_dict(dict):
    print('开始下载: %s %s ' % (dict.innerId, dict.text))

    # indexOfDict = next((i for i, item in enumerate(dicts) if str(item.innerId) == str(dict.innerId)), -1)
    #
    # originDict = dicts[indexOfDict]
    #
    # originDict.status = 'loading'

    downloadFilePath = '%s/%s/%s.bdict' % (downloadPath, dict.directory, dict.innerId)

    try:
        urllib.request.urlretrieve(dict.href, downloadFilePath)
    except:
        print('下载失败: %s %s ' % (dict.innerId, dict.text))

    # originDict.status = "loaded"
    # loaded = sum(1 for d in dicts if d.status == "loaded")
    print('下载完成: %s %s ' %(dict.innerId, dict.text))

def mkdir(path):
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        print(path, ' 创建成功')
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path, ' 目录已存在')
        return False


def start_parse(url):
    soup = loadPage(url)
    # soup = bs4.BeautifulSoup(response.text);

    if not os.path.exists(downloadPath):
        mkdir(downloadPath)
    
    for archive in soup.select("li p.sort-title a"):
        print(host + archive.attrs["href"])
        pinyinParts = pinyin(str(archive.get_text()).replace('\n', ''), style=Style.NORMAL)
        pinyinStr = [item for sublist in pinyinParts for item in sublist]
        tag = {
            "text": str(archive.get_text()).replace('\n', ''),
            "href": host + archive.attrs["href"],
            "pinyin": ''.join(pinyinStr),
            "status": "ready",
            "type": "category"
        }
        if not os.path.exists('%s/%s' % (downloadPath, tag['pinyin'])):
            mkdir('%s/%s' % (downloadPath, tag['pinyin']))
        if len(debug) < 1 or tag["text"] in debug:
            categories.append(tag)
            print('已识别 %s ' % tag["text"])
            processCategory(tag)
        else:
            print('Skip %s ' % tag["text"])

    print("搜索完成 %s " % len(dicts))
    download_dicts()

    for cate in categories:
        print('Parsering %s' % cate['text'])
        os.system("python ./tools/rime_dict_tool.py %s -o=./luna_pinyin.extended/luna_pinyin.baidu_%s.dict.yaml" % (
            "./download/%s/*.bdict" % cate['pinyin'],
            cate['pinyin'],
        ))

# 当命令行运行该模块时，__name__等于'__main__'
# 其他模块导入该模块时，__name__等于'parse_html'
if __name__ == '__main__':
    start_parse(archives_url)
