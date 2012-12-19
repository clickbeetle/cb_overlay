#!/bin/bash

dNow=`pwd` 
DIR=$1
cd ${DIR}
tree -dif -L 2 --noreport | gawk -F "/" '{print $2}' |grep -ie '-' -ie 'virtual' | uniq | gawk '{print "ls -1hd "$1"/*"}' | sh
cd ${dNow}