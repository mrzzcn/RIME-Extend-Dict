#!/usr/bin/env python
# -*- coding: utf-8 -*-

import struct
from . tools import BaseDictFile


#搜狗的scel词库就是保存的文本的unicode编码，每两个字节一个字符（中文汉字或者英文字母）
#找出其每部分的偏移位置即可
#主要两部分
#1.全局拼音表，貌似是所有的拼音组合，字典序
#       格式为(index,len,pinyin)的列表
#       index: 两个字节的整数 代表这个拼音的索引
#       len: 两个字节的整数 拼音的字节长度
#       pinyin: 当前的拼音，每个字符两个字节，总长len

#2.汉语词组表
#       格式为(same,py_table_len,py_table,{word_len,word,ext_len,ext})的一个列表
#       same: 两个字节 整数 同音词数量
#       py_table_len:  两个字节 整数
#       py_table: 整数列表，每个整数两个字节,每个整数代表一个拼音的索引
#
#       word_len:两个字节 整数 代表中文词组字节数长度
#       word: 中文词组,每个中文汉字两个字节，总长度word_len
#       ext_len: 两个字节 整数 代表扩展信息的长度，好像都是10
#       ext: 扩展信息 前两个字节是一个整数(不知道是不是词频) 后八个字节全是0
#
#      {word_len,word,ext_len,ext} 一共重复same次 同音词 相同拼音表
class scel(BaseDictFile):
    def __init__(self):
        BaseDictFile.__init__(self)
        # 文件头
        self.head = '\x40\x15\x00\x00\x44\x43\x53\x01\x01\x00\x00\x00'
        #拼音表偏移，
        self.start_pinyin     = 0x1540
        #汉语词组表偏移
        self.start_chinese    = 0x2628
        # 词库名
        self.dict_name        = ''
        # 词库分类
        self.dict_category    = ''
        # 词库描述
        self.dict_description = ''
        # 词库样例
        self.dict_sample      = ''


    #获取拼音表
    def _getPyTable(self, data):
        if data[0:4] != "\x9D\x01\x00\x00":
            return None
        data = data[4:]
        pos = 0
        length = len(data)
        while pos < length:
            index = struct.unpack('H',data[pos]+data[pos+1])[0]
            #print index,
            pos += 2
            l = struct.unpack('H',data[pos]+data[pos+1])[0]
            #print l,
            pos += 2
            py = byte2str(data[pos:pos+l])
            #print py
            self.pinyin_table[index]=py
            pos += l

    #获取一个词组的拼音
    def _getWordPy(self, data):
        pos = 0
        length = len(data)
        pinyin_list = []
        while pos < length:

            index = struct.unpack('H',data[pos]+data[pos+1])[0]
            pinyin_list.append(self.pinyin_table[index])
            pos += 2    
        return ' '.join(pinyin_list).encode('utf-8')

    #获取一个词组
    def _getWord(self, data):
        pos = 0
        length = len(data)
        pinyin_list = []
        while pos < length:

            index = struct.unpack('H',data[pos]+data[pos+1])[0]
            pinyin_list.append(self.pinyin_table[index])
            pos += 2
        return ' '.join(pinyin_list)

    #读取中文表
    def _getChinese(self, data):
        #import pdb
        #pdb.set_trace()

        pos = 0
        length = len(data)
        while pos < length:
            #同音词数量
            same = struct.unpack('H',data[pos]+data[pos+1])[0]
            #print '[same]:',same,

            #拼音索引表长度
            pos += 2
            py_table_len = struct.unpack('H',data[pos]+data[pos+1])[0]
            #拼音索引表
            pos += 2
            py = self._getWordPy(data[pos: pos+py_table_len])

            #中文词组
            pos += py_table_len
            for i in xrange(same):
                #中文词组长度
                c_len = struct.unpack('H',data[pos]+data[pos+1])[0]
                #中文词组
                pos += 2  
                word = byte2str(data[pos: pos + c_len])
                #扩展数据长度
                pos += c_len        
                ext_len = struct.unpack('H',data[pos]+data[pos+1])[0]
                #词频
                pos += 2
                count  = struct.unpack('H',data[pos]+data[pos+1])[0]

                w = Word()

                w.value = word.encode('utf-8')
                w.count = count

                #保存
                self.dictionary.add(py, w)

                #到下个词的偏移位置
                pos +=  ext_len


    def get_dict_info(self, data):

        self.dict_name        = byte2str(data[0x130:0x338]).encode(get_locale())
        self.dict_category    = byte2str(data[0x338:0x540]).encode(get_locale())
        self.dict_description = byte2str(data[0x540:0xd40]).encode(get_locale())
        self.dict_sample      = byte2str(data[0xd40:self.start_pinyin]).encode(get_locale())


    def load(self, filename):
        #解析结果
        #元组(词频,拼音,中文词组)的列表
        GTable = []

        #print '-'*60
        f = open(filename,'rb')
        data = f.read()
        f.close()

        if data[0:12] != self.head:
            # print "It's not a .scel file"
            sys.exit(1)

        return self.read(data)

    def read(self, data):
        #pdb.set_trace()
        self.get_dict_info(data[:self.start_pinyin])

        self._getPyTable(data[self.start_pinyin:self.start_chinese])
        self._getChinese(data[self.start_chinese:])
        return self.dictionary

