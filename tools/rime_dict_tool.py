#!/usr/bin/python
# -*- coding: utf-8 -*-


import struct
import sys
import binascii
import pdb
import os
import codecs
import mechanize, fileinput

from IME import *
from argparse import ArgumentParser

def argparser():
    parser = ArgumentParser(description="Convert from other word dictionary to RIME's yaml dictionary format, support multiple types.")
    parser.add_argument('-o', '--output', type=str, default='', help='Write ALL results to spicified file, otherwise write into separate files with original name.')
    parser.add_argument('files', nargs='+', type=str, help='Dictionary files')
    return parser.parse_args()


if __name__ == '__main__':

    parser = argparser()
    output = parser.output
    #将要转换的词库添加在这里就可以了
    files = parser.files
    d = tools.WordDict()
    for f in files:
        filename, fileext = os.path.splitext(os.path.basename(f))
        if fileext.lower() == '.scel':
            worddict = Sougou.scel()
        elif fileext.lower() == '.uwl':
            worddict = Ziguang.uwl()
        elif fileext.lower() == '.bdict':
            worddict = Baidu.bdict()
        elif fileext.lower() == '.txt':
            worddict = Thuocl.thuocl()
        else:
            raise Exception("File type not supported yet.")


        if not output:
            d = worddict.load(f)

            # 获取文件名
            output = "./luna_pinyin.extended/luna_pinyin." + filename + ".dict.yaml"
            d.dump(output)
        else:
            d.merge(worddict.load(f))
    if output:
        filename = os.path.splitext(os.path.basename(output))[0].split('.dict')[0]
        d.dump(output)

    existed = False
    importFileName = 'luna_pinyin.extended/' + filename;
    with codecs.open('./luna_pinyin.extended.dict.yaml', 'r', 'utf-8') as extended :
        lines = extended.readlines()
        existed = any(line.find(importFileName)>=0 for line in lines)

    print(existed)

    with codecs.open('./luna_pinyin.extended.dict.yaml', 'w', 'utf-8') as extended :
        for line in lines:
            extended.write(line)
            if line.find("  # network dict lib")>=0 and not existed:
                extended.write('  - ' + importFileName + '\n')

