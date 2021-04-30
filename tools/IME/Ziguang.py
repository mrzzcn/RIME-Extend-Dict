#!/usr/bin/env python
# -*- coding: utf-8 -*-

import struct
from . tools import BaseDictFile

class uwl(BaseDictFile):
    def __init__(self):
        BaseDictFile.__init__(self)
        self.hash = ''
        self.word_count = 0
        self.name = ''
        self.author = ''
        self.page_count = 0
        self.page_start = 0xc00
        self.page_length = 0x400
        # 声母表
        self.shengmu = [ "", "b", "c", "ch", "d", "f", "g", "h", "j", "k", "l", "m", "n",
            "p", "q", "r", "s", "sh", "t", "w", "x", "y", "z", "zh"]
        # 韵母表
        self.yunmu = [ "ang", "a", "ai", "an", "ang", "ao", "e", "ei", "en", "eng", "er",
            "i", "ia", "ian", "iang", "iao", "ie", "in", "ing", "iong", "iu", "o", "ong",
            "ou", "u", "ua", "uai", "uan", "uang", "ue", "ui", "un", "uo", "v"]
        # 标点符号列表
        self.symbols = [u'\u2018', u'\u2019', u'\uff0c', u'\u3002', u'\uff01', u'\uff1f',
        u'\u2026', u'\uff08', u'\uff09', u'\uff1a', u'\u300a', u'\u300b', u'\u201c',
        u'\u201d']

    def get_dict_info(self, data):
        #typedef struct WORDLIBHEADER
        #{
        #	int			signature;							//词库的签名
        #	TCHAR		name[WORDLIB_NAME_LENGTH];			//词库的名称
        #	TCHAR		author_name[WORDLIB_AUTHOR_LENGTH];	//词库作者名称
        #	int			word_count;							//词汇数目
        #	int			page_count;							//已分配的页数
        #	int			can_be_edit;						//是否可以编辑
        #	int			pim_version;						//输入法版本号（兼容性考虑）
        #	int			index[CON_NUMBER][CON_NUMBER];		//索引表
        #}
        # 0~3字节是词库的hash值
        self.signature = struct.unpack('I', data[:4])
        # 4~35  字节：词库名
        # 36~67 字节：词库作者名
        self.name = byte2str(data[4:36]).rstrip('\x00')
        self.author = byte2str(data[36:68]).rstrip('\x00')
        # 68~71 字节：词汇数量
        # 72~75 字节：已分配的页面（page）数量
        # 76~89 字节：是否可写的标识位
        # 80~83 字节：输入法版本号
        # 剩下的3020字节不清楚是什么，有大量的空白
        self.word_count = struct.unpack('I',data[68:72])[0]
        self.page_count = struct.unpack('I',data[72:76])[0]
        self.editable = struct.unpack('I',data[76:80])[0]
        self.version = struct.unpack('I',data[80:84])[0]
        return self.name, self.author, self.word_count, self.page_count

#    def _parse(self, data):
#        # 没搞懂这玩意是干嘛的
#        len_code_dict = [0x05, 0x87, 0x09, 0x8B, 0x0D, 0x8F, 0x11, 0x13, 0x15, 0x17, 0x19]
#        pos = 0
#        word = Word()
#        len_code = struct.unpack('B', data[pos])[0]
#        pos += 1
#        try:
#            length = len_code_dict.index(len_code) + 2
#        except ValueError:
#            print(repr(data))
#        len_byte = length * 4 + 4
#        # 计算词汇的权重，算法看起来很奇葩的样子
#        rank = struct.unpack('I', ''.join(struct.unpack('3c', data[pos:pos+3])) + '\x00')[0]
#        pos += 3
#        count = (rank - 1) / 32
#        # 计算拼音长度，最多允许8字节长度的拼音
#        if length <= 8:
#            pinyin_len = length
#        else:
#            pinyin_len = 8
#        pinyin = []
#        for i in xrange(pinyin_len):
#            # 计算声母编码
#            sm = struct.unpack('B', data[pos])[0]
#            sm_index = sm & 31
#            pos += 1
#            # 计算韵母编码
#            ym = struct.unpack('B', data[pos])[0]
#            ym_index = (sm >> 5) + (ym << 3)
#            pos += 1
#            # 从计算出来的拼音编码查询对应的拼音字母
#            try:
#                pinyin.append(self.shengmu[sm_index] + self.yunmu[ym_index])
#            except:
#                pass
#        word.pinyin = ' '.join(pinyin)
#
#        # 查询汉字
#        word.value = data[pos:pos+length*2]
#
#        return (word, len_byte)
#
#
#    def _parse_page(self, data):
#        # page 单独取出来处理
#        pos = 0
#        # 0~3字节是索引编号（page的编号，对应上面的page_count），从0开始计数
#        # 4~7字节不知道是什么
#        # 8~11字节不知道是干嘛的，从深蓝的代码里抄的变量名
#        # 12~15字节是page的实际内容长度
#        index_number, unknown, word_len_enums, word_byte_len = struct.unpack('4I', data[pos:pos+16])
#        print("-"*60)
#        print(repr(data))
#
#        # 开始读取page中的有效内容，直到 length_read == word_byte_len
#        pos = 16
#        length_read = 0
#        while length_read < word_byte_len:
#            word, l = self._parse(data[pos:])
#            length_read += l
#            pos = pos + l
#            if self.dictionary.has_key(word.pinyin):
#                self.dictionary[word.pinyin].append(word)
#            else:
#                self.dictionary[word.pinyin] = []
#                self.dictionary[word.pinyin].append(word)

#    def _len_code(self, data):
#        read_byte = 0
#        valid = False
#        len_code = struct.unpack('B', data[read_byte])[0]
#        read_byte += 1

    # def _len_code(self, data):
    #     read_byte = 0
    #     valid = False
    #     while not valid:
    #         len_code = struct.unpack('B', data[read_byte])[0]
    #         next_len_code = struct.unpack('B', data[read_byte+1])[0]
    #         read_byte += 1
    #         if (len_code in self.len_code_dict) and not (next_len_code in self.len_code_dict):
    #             valid = True
    #             break
    #         else:
    #             read_byte += 1
    #         #if read_byte >= len(data) or read_byte > length_limit:
    #         if read_byte >= len(data):
    #                 break
    #     if len_code not in self.len_code_dict:
    #         print('---------------------')
    #         print(repr(data))
    #
    #     if len_code == 0 :
    #         length = None
    #         read_byte = len(data)
    #     else:
    #         length = self.len_code_dict.index(len_code) + 2
    #         length_limit = 1 + 3 + length * 4 + length * 4
    #         if length_limit >= len(data[read_byte:]):
    #             length = None
    #             read_byte = len(data)
    #
    #     return (len_code, length, read_byte)

    def _len_code(self, data):
        read_byte = 0
        len_code = struct.unpack('B', data[read_byte])[0]
        length = 1 + 3 + (self.len_code_dict.index(len_code) + 2)*4
        effective = struct.unpack('B', data[read_byte+3])[0]
        return(length,effective)

    def _get_pinyin_str(self, data, pinyin_len):
        # 读取音节
        pinyin = []
        pos = 0
        for i in xrange(pinyin_len):
            # 计算声母编码
            sm = struct.unpack('B', data[pos])[0]
            # try:
            #     sm = struct.unpack('B', data[pos])[0]
            # except IndexError:
            #     print(repr(data))
            sm_index = sm & 31
            pos += 1
            # 计算韵母编码
            ym = struct.unpack('B', data[pos])[0]
            # try:
            #     ym = struct.unpack('B', data[pos])[0]
            # except IndexError:
            #     print(repr(data))
            ym_index = (sm >> 5) + (ym << 3)
            pos += 1
            # 从计算出来的拼音编码查询对应的拼音字母
            try:
                pinyin.append(self.shengmu[sm_index] + self.yunmu[ym_index])
            except:
                pass
        return ' '.join(pinyin)

    def _parse(self, data):
        read_byte = 0
        word = Word()
        # length, read_byte = self._len_code(data)
        # 如果self._len_code 函数返回 None，表示剩余的数据中没有找到len_code，直接返回，不做解析
        worditem_head = bin(struct.unpack('!I', data[read_byte:read_byte+4])[0])[2:].zfill(32)
        read_byte += 4
        # 读取effective位
        effective = worditem_head[0]
        length = int(worditem_head[1:7],2)
        # 词库中的pinyin_len是垃圾值，扔掉
        pinyin_len = int(worditem_head[7:13],2)

        # FIXME: 词库中有些拼音长度很奇怪的词，目前没找到处理方式，先扔掉读到的拼音长度，参考词长估算拼音长度
        if length != pinyin_len:
            # 如果拼音长度大于词长，读取到的拼音长度是错的，以词长覆盖
            if length < pinyin_len:
                pinyin_len = length
            # 如果是词长大于拼音长度，通常是词汇中含有标点符号造成的，先放过
            if length > pinyin_len:
                pass

        # 词汇的权重
        count = int(worditem_head[13:32],2)

        # FIXME: 这个变量是留在后面给汉字内容检查用的
        tmp = pinyin_len

        # FIXME: 提前对汉字内容做检查。紫光词库中包含有带标点符号的词汇，造成词汇长度跟
        # 音节长度不对应，需要提前处理以防错位。这是一个workaround。
        hanzi_len = length*2
        if pinyin_len > 8:
            hanzi = byte2str(data[read_byte + 8*2:read_byte + 8*2 + hanzi_len])
        else:
            hanzi = byte2str(data[read_byte + pinyin_len*2:read_byte + pinyin_len*2 + hanzi_len])
        for i in hanzi:
            if (i in self.symbols):
                pinyin_len -= 1
        print('-'*60)
        print(pinyin_len, length,hanzi)

        # 计算拼音长度，最多允许8个音符长度的拼音
        if pinyin_len > 8:
            pinyin_len = 8

        # 读取音节
        word.pinyin = self._get_pinyin_str(data[read_byte:read_byte + pinyin_len * 2], pinyin_len)

        read_byte += pinyin_len * 2
        # debug: 计算最大长度
        #           len_code + rank + pinyin + hanzi
        # 查询汉字
        # FIXME: 紫光uwl文件的解析有点问题，目前使用的解析规则并不能完全正确的解析出所有内容，所以需要验证获取到的词汇是否在汉字范围之内（包括ASCII英文）
        hanzi_len = length*2
        hanzi = byte2str(data[read_byte:read_byte+hanzi_len])
        read_byte += hanzi_len
        if is_cjk(hanzi):
            word.value = hanzi.encode('utf-8')

        #print('len_code: ' + repr(len_code) + '\t' + 'length/read_byte: ' + repr(length) + '/' + repr(read_byte) + '\t' + 'count: ' + repr(count) + '\t' + 'next_len_code: ' + '\t' + repr(next_len_code))
        print(str(len(data[0:read_byte]))  + repr((length, pinyin_len)) + '\t' + repr(data[0:read_byte]) + '--->' + word.value + '\t' + ':' +'\t' + word.pinyin)
        return (word, read_byte)

    def _parse_page(self, data):
        #typedef	struct PAGE
        #{
        #	int			page_no;							//页号
        #	int			next_page_no;						//下一个页号，-1标识结束
        #	int			length_flag;						//本页包含的词汇长度的标志
        #	int			data_length;						//已经使用的数据长度
        #	char		data[WORDLIB_PAGE_DATA_LENGTH];		//数据开始
        #} PAGE;
        # page 单独取出来处理
        pos = 0
        # 0~3字节是索引编号（page的编号，对应上面的page_count），从0开始计数
        # 4~7字节不知道是什么
        # 8~11字节不知道是干嘛的，从深蓝的代码里抄的变量名
        # 12~15字节是page的实际内容长度
        index_number, unknown, word_len_enums, word_byte_len = struct.unpack('4I', data[pos:pos+16])
        #print("-"*60)
        #print(repr(data))

        # 开始读取page中的有效内容，直到 length_read == word_byte_len
        pos = 16
        length_read = 0
        while length_read < word_byte_len:
            word, l = self._parse(data[pos:])
            length_read += l
            old_pos = pos
            pos = pos + l
            if word.value:
                if self.dictionary.has_key(word.pinyin):
                    self.dictionary[word.pinyin].append(word)
                else:
                    self.dictionary[word.pinyin] = []
                    self.dictionary[word.pinyin].append(word)
            else:
                print(repr(data[old_pos:pos]))
        return self.dictionary

    def load(self, filename):
        f = open(filename, 'rb')
        data = f.read()
        f.close()
        return self.read(data)

    def read(self, data):
        self.get_dict_info(data)
        for i in xrange(self.page_count):
            # debug
            print('page: ' + str(i))
            pos = self.page_start + self.page_length * i
            self._parse_page(data[pos:pos+self.page_length])
#            try:
#                self._parse_page(data[pos:pos+self.page_length])
#            except ValueError, e:
#                print(repr(data[pos:pos+self.page_length]))
#                raise Exception(e)
        return self.dictionary
