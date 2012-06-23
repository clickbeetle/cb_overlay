# Copyright 2010 Funtoo Technologies
# Distributed under the terms of the GNU General Public License v2

EAPI="4-python"

PYTHON_MULTIPLE_ABIS="1"
PYTHON_RESTRICTED_ABIS="2.5 3.1 *-jython *-pypy-*"

inherit multilib python

DESCRIPTION="Funtoo Core Boot Framework for global boot loader configuration"
HOMEPAGE="http://www.funtoo.org/en/funtoo/core/boot"
LICENSE="GPL-3"
SLOT="0"
KEYWORDS="~*"
RESTRICT="mirror"
GITHUB_REPO="boot-update"
GITHUB_USER="funtoo"
GITHUB_TAG="${PV}"
SRC_URI="https://www.github.com/${GITHUB_USER}/${GITHUB_REPO}/tarball/${GITHUB_TAG} -> boot-update-${GITHUB_TAG}.tar.gz"

IUSE=""

DEPEND=""
RDEPEND=">=sys-boot/grub-1.98-r2"

src_unpack() {
	unpack ${A}
	mv "${WORKDIR}/${GITHUB_USER}-${PN}"-??????? "${S}" || die
}

src_install() {
	insinto /usr/$(get_libdir)/`eselect python show --python2`/site-packages
	cd ${S}/python/modules
	doins -r .

	cd ${S}

	dodoc doc/*.rst

	doman doc/boot-update.8
	doman doc/boot.conf.5

	into /
	dosbin sbin/boot-update

	dodoc etc/boot.conf.example
	insinto /etc
	doins etc/boot.conf
	doins etc/boot.conf.defaults
}

src_compile() {
	return
}
