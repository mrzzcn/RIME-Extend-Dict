#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Author: Jack
# @Date:   2018-06-06 16:28:49
# @Last Modified by:   Jack
# @Last Modified time: 2018-06-06 16:29:04

import struct
from . tools import BaseDictFile
import binascii

class thuocl(BaseDictFile):
    def __init__(self):
        BaseDictFile.__init__(self)

        self.fenmu = ["c", "d", "b", "f", "g", "h", "ch", "j", "k", "l", "m", "n", "", "p", "q", "r", "s", "t", "sh",
                      "zh", "w", "x", "y", "z"]
        self.yunmu = [ "uang", "iang", "ong", "ang", "eng", "ian", "iao", "ing", "ong", "uai", "uan", "ai", "an", "ao",
                       "ei","en", "er", "ua", "ie", "in", "iu", "ou", "ia", "ue", "ui", "un", "uo", "a", "e", "i", "a", "u", "v"]
        pass

    def hexToWord(self, hexStr):
        wordList = []
        for i in range(0, len(hexStr), 4):
            word = (chr(int(hexStr[i:i+2], 16)) + chr(int(hexStr[i+2:i+4], 16))).decode('utf-16')
            if u'\u4e00' <= word <= u'\u9fa5':
                word = word.encode("utf-8")
                wordList.append(word)
            else:
                wordList = []
                break
        return wordList

    def hexToPinyin(self, hexString):
        pinyinList = []
        for i in range(0, len(hexString), 4):
            fenmu = self.fenmu[int(hexString[i:i+2], 16)]
            yunmu = self.yunmu[int(hexString[i+2:i+4], 16)]
            pinyinList.append(fenmu+yunmu)
        return pinyinList

    def read(self, content):
        # print "reading"
        # print content
        words = content.split("\n");
        index = 0
        total = len(words)
        word = Word()
        
        # 过滤前面信息
        while index < total:
            wordParts = words[index].split("\t")
            if len(wordParts) != 2 :
              break
            word.value = wordParts[0].replace(" ", "")
            word.count = int("0" + wordParts[1].replace(" ", ""))
            word.pinyin = ""
            if self.dictionary.has_key(word.pinyin):
                self.dictionary[word.pinyin].append(word)
            else:
                self.dictionary[word.pinyin] = []
                self.dictionary[word.pinyin].append(word)
            index = index + 1
            word = Word()

    def load(self, filename):
        wordList = []
        fileText = open(filename, "rb")
        with fileText as f:
            content = f.read()
        self.read(content)
        return self.dictionary
