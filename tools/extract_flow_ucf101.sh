#!/usr/bin/env bash

export classFile=../data/ucf101/videos/filelist.txt

for line in $(cat $classFile)
do
    echo "We are processing $line !"
    cd ../data/ucf101/videos/$line
    ls | tail -n +2 > filelist.txt
    cd ../../../../
    python tools/flow_extraction.py --input data/ucf101/videos/$line/filelist.txt --prefix data/ucf101/videos/$line/ --dest data/ucf101/rawframes/$line/
    echo "$line has been processed !"
done