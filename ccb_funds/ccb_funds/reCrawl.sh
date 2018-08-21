#!/bin/bash
#
# 这个脚本将list中的所有数据都爬一遍
echo
if [ -d './result' ]; then
    rm -rf result/*.csv
else
    mkdir result
fi
bankList=(icbc abc ccb boc bcm cib spdb ceb cmbc cgb hxb pingan citicbank czb hfbank)
for bank in ${bankList[@]};
do
    scrapy crawl $bank
done