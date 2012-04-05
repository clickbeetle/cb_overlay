#!/bin/bash
eval `keychain --noask --eval id_dsa`  || exit 1
cd /root/git/funtoo-overlay
# get latest merge.py and friends
git pull || exit 1
/root/git/funtoo-overlay/funtoo/scripts/merge.py --branch experimental /BACKUP/clickbeetleCook.DO_NO_DELETE/git/experimental-mini-2011 || exit 1
