#!/usr/local/bin/bash

python ./tools/baiduspider.py
python ./tools/rime_dict_tool.py ./download/*.bdict -o=./luna_pinyin.extended/luna_pinyin.baidu_dicts.dict.yaml
