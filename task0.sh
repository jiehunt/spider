#! /bin/sh
source ~/.profile
PATH=~/tools/anaconda3/bin/:$PATH
output=$(python ~/work/task/spider.py)
echo $output
output=$(python ~/work/task/mypush.py)
echo $output
