#!/usr/bin/python
# -*- coding: utf-8 -*-


import struct
import sys
import binascii
import pdb
import os
import codecs
from IME import tools, Sougou, Baidu, Ziguang, Thuocl
# from IME import *
from argparse import ArgumentParser
from multiprocessing import Pool, cpu_count
from multiprocessing.managers import BaseManager
import threading
import functools
import tqdm

share_lock = threading.Lock()


def argparser():
    parser = ArgumentParser(
        description="Convert from other word dictionary to RIME's yaml dictionary format, support multiple types.")
    parser.add_argument('-o', '--output', type=str, default='',
                        help='Write ALL results to spicified file, otherwise write into separate files with original name.')
    parser.add_argument('files', nargs='+', type=str, help='Dictionary files')
    return parser.parse_args()


def processDict(dictFile, finalDicts):
    global share_lock

    # print('%s/%s %s' % (poolProgress.pos, poolProgress.total, dictFile))
    filename, fileext = os.path.splitext(os.path.basename(dictFile))
    if fileext.lower() == '.scel':
        wordDict = Sougou.scel()
    elif fileext.lower() == '.uwl':
        wordDict = Ziguang.uwl()
    elif fileext.lower() == '.bdict':
        wordDict = Baidu.bdict()
    elif fileext.lower() == '.txt':
        wordDict = Thuocl.thuocl()
    else:
        raise Exception("File type not supported yet.")
    share_lock.acquire()
    finalDicts.merge(wordDict.load(dictFile))
    share_lock.release()


if __name__ == '__main__':
    parser = argparser()
    output = parser.output
    # 将要转换的词库添加在这里就可以了
    files = parser.files
    total = len(files)
    manager = BaseManager()
    manager.register('WordDict', tools.WordDict)
    manager.start()
    finalDicts = manager.WordDict()

    processor = functools.partial(processDict, finalDicts=finalDicts)
    with Pool(processes=cpu_count() - 1) as pool:
        r = list(tqdm.tqdm(pool.imap_unordered(processor, files), total=total))
        if output:
            filename = os.path.splitext(os.path.basename(output))[0].split('.dict')[0]
            finalDicts.dump(output)

    existed = False
    importFileName = 'luna_pinyin.extended/' + filename;
    with codecs.open('./luna_pinyin.extended.dict.yaml', 'r', 'utf-8') as extended:
        lines = extended.readlines()
        existed = any(line.find(importFileName) >= 0 for line in lines)

    if existed == True:
        print('Already listed in config.')
    else:
        with codecs.open('./luna_pinyin.extended.dict.yaml', 'w', 'utf-8') as extended:
            for line in lines:
                extended.write(line)
                if line.find("  # network dict lib") >= 0 and not existed:
                    extended.write('  - ' + importFileName + '\n')
                    print('Listed in config.')
