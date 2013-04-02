# Copyright 2008-2012 Funtoo Technologies
# Distributed under the terms of the GNU General Public License v2
# $Header: $

EAPI="4"

inherit eutils

DESCRIPTION="Spark is a XMPP client that works with openfire servers"
HOMEPAGE="http://www.igniterealtime.org/projects/spark/index.jsp"
SRC_URI="http://www.igniterealtime.org/downloadServlet?filename=spark/spark_2_6_3.tar.gz"
LICENSE="Apache-2.0"
SLOT="0"
KEYWORDS="~x86 amd64"

DEPEND=""

RDEPEND="${DEPEND}"
S="${WORKDIR}/Spark"


src_unpack() {
	unpack ${A} 
}

src_install() {
	dodir /opt/Spark
	cp -pPR $S $D/opt/ || die "Install Failed"
	dobin ${FILESDIR}/spark
}

pkg_postinst()
{
    	chmod 777 /opt/Spark -Rv
}
