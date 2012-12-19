#!/bin/bash

eval `keychain --noask --eval id_dsa`  || exit 1

# This is the rsync mirror where we grab Portage updates from...
src=rsync://ftp.iij.ad.jp/pub/linux/gentoo/

# This is the target directory for our updates...
dst=/BACKUP/clickbeetleDistfiles.DO_NO_DELETE/

cd $dst || exit 1

# Now, use rsync to write new changes directly on top of our working files. New files will be added, deprecated files will be deleted.
rsync --recursive --links --safe-links --perms --times --compress --force --whole-file --timeout=180 --exclude=/.git -v --progress ${src}distfiles/ $dst || exit 1
# We want to make extra-sure that we don't grab any metadata, since we don't keep metadata for the gentoo.org tree (space reasons)
exit 0
