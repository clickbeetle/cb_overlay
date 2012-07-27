#!/bin/bash
touch /BACKUP/clickbeetleCook.DO_NO_DELETE/tmp/.regen_running
eval `keychain --noask --eval id_rsa`  || exit 1

die() {
	echo $*
	rm -f /BACKUP/clickbeetleCook.DO_NO_DELETE/tmp/.regen_running
	exit 1
}
cd /BACKUP/clickbeetleCook.DO_NO_DELETE/git/cb_overlay || die "couldn't chdir"
git pull
#./funtoo/scripts/gentoo-update.sh || die "gentoo update failed"
#./funtoo/scripts/cb-sync-upstream.py /BACKUP/clickbeetleCook.DO_NO_DELETE/git/cb_overlay || die "cb_overlay update failed"
./funtoo/scripts/merge.py /BACKUP/clickbeetleCook.DO_NO_DELETE/git/cb_ports || die "funtoo update failed cb_ports"
#./funtoo/scripts/cb_cpl_syncEbuilds.py --branch=studio /BACKUP/clickbeetleCook.DO_NO_DELETE/git/cb_ports_locked || die "funtoo update failed cpl"
rm -f /BACKUP/clickbeetleCook.DO_NO_DELETE/tmp/.regen_running
