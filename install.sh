#!/usr/local/bin/bash

token="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"

release=$(curl -H "Authorization: token $token" https://api.github.com/repos/mrzzcn/RIME-Extend-Dict/releases/latest | grep 'Dicts' | grep 'browser_' | cut -d\" -f4);

curl -L -H "Authorization: token $token" "$release" --output Dicts.zip

unzip -qq Dicts.zip
rm Dicts.zip

cp -r luna_pinyin.extended $HOME/Library/Rime/
cp luna_pinyin.extended.dict.yaml $HOME/Library/Rime/

osascript -e '
display notification "Download & Install successfully, Deploy by Click Icon -> Deploy." with title "Squirrel"
'