#!/bin/bash
eval `keychain --noask --eval id_dsa`  || exit 1
cd /root/git/funtoo-overlay
# get latest merge.py and friends
git pull || exit 1
/root/git/funtoo-overlay/funtoo/scripts/merge.py --branch master /BACKUP/clickbeetleCook.DO_NO_DELETE/git/portage-mini-2011 /BACKUP/clickbeetleCook.DO_NO_DELETE/git/ports-2012 || exit 1
