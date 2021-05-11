#!/usr/local/bin/bash

DICTS_DIRECTORY=$(mktemp -d)

# release=http://127.0.0.1/Dicts.zip
release=https://github.com/mrzzcn/RIME-Extend-Dict/releases/latest/download/Dicts.zip

curl -L $release --output "$DICTS_DIRECTORY/Dicts.zip"

cp -r $HOME/Library/Rime/luna_pinyin.extended.dict.yaml $HOME/Library/Rime/luna_pinyin.extended.dict.yaml.bak

echo '~/Library/Rime/luna_pinyin.extended.dict.yaml backed up to: ~/Library/Rime/luna_pinyin.extended.dict.yaml.bak'

echo "Unzip: $DICTS_DIRECTORY/Dicts.zip"
unzip -qq "$DICTS_DIRECTORY/Dicts.zip" -d "$DICTS_DIRECTORY"

echo "Installing..."
cp -r "$DICTS_DIRECTORY/luna_pinyin.extended" $HOME/Library/Rime/
cp "$DICTS_DIRECTORY/luna_pinyin.extended.dict.yaml" $HOME/Library/Rime/

echo "Clean up: $DICTS_DIRECTORY"
rm -rf "$DICTS_DIRECTORY/"

osascript -e '
display notification "Download & Install successfully, Deploy by Click Icon -> Deploy." with title "Squirrel"
'