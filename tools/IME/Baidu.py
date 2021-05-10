#!/usr/bin/env python
# -*- coding: utf-8 -*-

import struct
from .tools import *
import binascii


class bdict(BaseDictFile):
    def __init__(self):
        BaseDictFile.__init__(self)

        self.fenmu = ["c", "d", "b", "f", "g", "h", "ch", "j", "k", "l", "m", "n", "", "p", "q", "r", "s", "t", "sh",
                      "zh", "w", "x", "y", "z"]
        self.yunmu = ["uang", "iang", "ong", "ang", "eng", "ian", "iao", "ing", "ong", "uai", "uan", "ai", "an", "ao",
                      "ei", "en", "er", "ua", "ie", "in", "iu", "ou", "ia", "ue", "ui", "un", "uo", "a", "e", "i", "a",
                      "u", "v"]
        pass

    def hexToWord(self, hexStr):
        wordList = []
        for i in range(0, len(hexStr), 4):
            if len(hexStr[i:i + 4]) < 4:
                break
            word = binascii.a2b_hex(hexStr[i:i + 4]).decode('utf-16')
            if u'\u4e00' <= word <= u'\u9fa5':
                wordList.append(word)
            else:
                wordList = []
                break
        return wordList

    def hexToPinyin(self, hexString):
        pinyinList = []
        for i in range(0, len(hexString), 4):
            fenmu = self.fenmu[int(hexString[i:i + 2], 16)]
            yunmu = self.yunmu[int(hexString[i + 2:i + 4], 16)]
            pinyinList.append(fenmu + yunmu)
        return pinyinList

    def read(self, content):
        hexData = binascii.hexlify(content)
        hexData = hexData[1696:]
        text = ""
        word = Word()
        # 过滤前面信息
        while True:
            wordCount = hexData[0:2]
            if len(wordCount) < 1:
                break
            wordCount = int(wordCount, 16)
            text = hexData[8 + wordCount * 4:8 + wordCount * 8]
            text = self.hexToWord(text)
            # print('Read: %s' % text)
            if len(text) < 1:
                break
            pinyin = hexData[8:8 + wordCount * 4]
            pinyin = self.hexToPinyin(pinyin)
            word = Word()
            word.value = "".join(text)
            word.pinyin = " ".join(pinyin)
            if word.pinyin in self.dictionary:
                self.dictionary[word.pinyin].append(word)
            else:
                self.dictionary[word.pinyin] = []
                self.dictionary[word.pinyin].append(word)
            hexData = hexData[8 + wordCount * 8:]
            if len(hexData) < 1:
                break

    def load(self, filename):
        wordList = []
        fileText = open(filename, "rb")
        with fileText as f:
            content = f.read()
        self.read(content)
        # print('Read complete: %s items total' % len(self.dictionary.keys()))
        return self.dictionary
