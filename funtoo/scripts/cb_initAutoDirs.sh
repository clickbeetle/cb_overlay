#!/bin/bash

if [ ! -d /BACKUP/clickbeetleCook.DO_NO_DELETE/git/ ]; then 
	mkdir -p /BACKUP/clickbeetleCook.DO_NO_DELETE/git/
fi

if [ ! -d /BACKUP/clickbeetleCook.DO_NO_DELETE/git/source-trees/ ]; then
	mkdir -p /BACKUP/clickbeetleCook.DO_NO_DELETE/git/source-trees/
fi

cd /BACKUP/clickbeetleCook.DO_NO_DELETE/git/

if [ ! -d /BACKUP/clickbeetleCook.DO_NO_DELETE/git/cb_ports/ ]; then
	git clone git@github.com:clickbeetle/cb_ports.git
else
	cd /BACKUP/clickbeetleCook.DO_NO_DELETE/git/cb_ports/
	git pull
	cd /BACKUP/clickbeetleCook.DO_NO_DELETE/git/
fi

if [ ! -d /BACKUP/clickbeetleCook.DO_NO_DELETE/git/cb_ports_locked/ ]; then
	git clone git@github.com:clickbeetle/cb_ports_locked.git
else
	cd /BACKUP/clickbeetleCook.DO_NO_DELETE/git/cb_ports_locked/
	git pull
	cd /BACKUP/clickbeetleCook.DO_NO_DELETE/git/

if [ ! -d /BACKUP/clickbeetleCook.DO_NO_DELETE/git/cb_gentoo/ ]; then
	git clone git@github.com:clickbeetle/cb_gentoo.git
else
	cd /BACKUP/clickbeetleCook.DO_NO_DELETE/git/cb_gentoo/
	git pull 
	cd /BACKUP/clickbeetleCook.DO_NO_DELETE/git/
fi

