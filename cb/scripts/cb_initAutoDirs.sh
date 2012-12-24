#!/bin/bash

if [ ! -d /BACKUP/clickbeetleCook.DO_NO_DELETE/git/ ]; then 
	mkdir -p /BACKUP/clickbeetleCook.DO_NO_DELETE/git/
fi

if [ ! -d /BACKUP/clickbeetleCook.DO_NO_DELETE/git/source-trees/ ]; then
	mkdir -p /BACKUP/clickbeetleCook.DO_NO_DELETE/git/source-trees/
fi

cd /BACKUP/clickbeetleCook.DO_NO_DELETE/git/

if [ ! -d /BACKUP/clickbeetleCook.DO_NO_DELETE/git/cb_ports/ ]; then
	echo "cloning cb_ports"
	git clone git@github.com:clickbeetle/cb_ports.git
fi

if [ ! -d /BACKUP/clickbeetleCook.DO_NO_DELETE/git/cb_ports_lts/ ]; then
	echo "cloning cb_ports_lts"
	git clone git@github.com:clickbeetle/cb_ports_lts.git
fi

if [ ! -d /BACKUP/clickbeetleCook.DO_NO_DELETE/git/cb_gentoo/ ]; then
	echo "cloning cb_gentoo"
	git clone git@github.com:clickbeetle/cb_gentoo.git
fi

