# Copyright 2008-2012 Funtoo Technologies
# Distributed under the terms of the GNU General Public License v2
# $Header: $

EAPI="4"

inherit eutils

DESCRIPTION="knotification is a perl plugin for pidgin to use the knotify backend"
HOMEPAGE="https://code.google.com/p/pidgin-knotifications/"
SRC_URI="http://distfiles.clickbeetle.in/knotifications-0.3.6.tar.gz"
SLOT="0"
KEYWORDS="x86 amd64"

DEPEND=""

RDEPEND="${DEPEND}"
S=$WORKDIR

src_unpack() {
        unpack ${A} 
}
        
        
src_install() {
	dodir /usr/lib/pidgin/
	cp -pPR ${WORKDIR}/* $D/usr/lib/pidgin/ || die "Install Failed"
}

