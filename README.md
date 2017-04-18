# RIME-Extend-Dict

Extend word dictionaries &amp; dict import tool for RIME input method   
扩展 Rime 输入法词库

## 0. clone the repo
` git clone git@github.com:mrzzcn/RIME-Extend-Dict.git`

## 1. 从百度词库下载词典

```bash
cd RIME-Extend-Dict

python ./tools/baiduspider.py
# 可以修改源文件 下载自己想要的分类词库
```

## 2. 转换词典格式
```bash
python ./tools/rime_dict_tool.py ./download/*.bdict -o=./luna_pinyin.extended/luna_pinyin.baidu_dicts.dict.yaml
```

## 3. 完成 部署

```
# 建议在部署之前先备份自己的当前配置

./tools/install
# 其实就是复制相关配置文件到 Rime 目录里面
# 完成之后点击 Rime 菜单的重新部署, 完成即可
```

## 4. 完成效果
![完成效果](https://raw.githubusercontent.com/mrzzcn/RIME-Extend-Dict/master/sample/sample.gif)
