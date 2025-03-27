#!/usr/bin/env bash

export classFile=../data/ucf101/rawframes/filelist.txt

for line in $(cat $classFile)
do
    echo "We are processing $line !"
    cd ../data/ucf101/rawframes/$line
    ls | tail -n +2 > filelist.txt
    cd ../../../../
    python tools/stackFlowChannel.py --input data/ucf101/rawframes/$line/filelist.txt --prefix data/ucf101/rawframes/$line/ --dest data/ucf101/rawframes_flow/$line/
    echo "$line has been processed !"
done