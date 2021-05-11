#!/usr/local/bin/bash

curl -L https://github.com/mrzzcn/RIME-Extend-Dict/releases/latest/download/Dicts.zip --output Dicts.zip

unzip -qq Dicts.zip
rm Dicts.zip

cp -r luna_pinyin.extended $HOME/Library/Rime/
cp luna_pinyin.extended.dict.yaml $HOME/Library/Rime/

osascript -e '
display notification "Download & Install successfully, Deploy by Click Icon -> Deploy." with title "Squirrel"
'