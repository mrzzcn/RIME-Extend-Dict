#!/usr/local/bin/bash

cp -r luna_pinyin.extended $HOME/Library/Rime/
cp luna_pinyin.extended.dict.yaml $HOME/Library/Rime/
cp luna_pinyin_simp.custom.yaml $HOME/Library/Rime/

osascript -e 'tell application "System Events" to key code 50 using {control down, option down}'
