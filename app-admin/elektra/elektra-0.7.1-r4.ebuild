# Copyright 1999-2013 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: /var/cvsroot/gentoo-x86/app-admin/elektra/elektra-0.7.1-r4.ebuild,v 1.1 2013/04/22 14:17:35 xmw Exp $

EAPI=5

inherit autotools autotools-multilib eutils multilib

DESCRIPTION="universal and secure framework to store config parameters in a hierarchical key-value pair mechanism"
HOMEPAGE="http://freedesktop.org/wiki/Software/Elektra"
SRC_URI="ftp://ftp.markus-raab.org/${PN}/${P}.tar.gz"

LICENSE="BSD"
SLOT="0"
KEYWORDS="~amd64 ~x86"
IUSE="gcov iconv static-libs test"

RDEPEND="!amd64? ( dev-libs/libxml2 )
	amd64? (
		abi_x86_64? ( dev-libs/libxml2 )
		abi_x86_32? ( app-emulation/emul-linux-x86-baselibs ) )"
DEPEND="${RDEPEND}
	!amd64? ( sys-devel/libtool )
	amd64? ( abi_x86_64? ( sys-devel/libtool ) )
	iconv? ( virtual/libiconv )
	!amd64? ( test? ( dev-libs/libxml2[static-libs] ) )"

src_prepare() {
	einfo 'Removing bundled libltdl'
	rm -rf libltdl || die

	epatch \
		"${FILESDIR}"/${P}-test.patch \
		"${FILESDIR}"/${P}-ltdl.patch \
		"${FILESDIR}"/${P}-automake-1.12.patch \
		"${FILESDIR}"/${P}-remove-ddefault-link.patch

	touch config.rpath
	eautoreconf
}

src_configure() {
	# berkeleydb, daemon, fstab, gconf, python do not work
	# avoid collision with kerberos (bug 403025, 447246)
	local myeconfargs=(
		--enable-filesys
		--enable-hosts
		--enable-ini
		--enable-passwd
		--disable-berkeleydb
		--disable-fstab
		--disable-gconf
		--disable-daemon
		--enable-cpp
		--disable-python
		$(use_enable gcov)
		$(use_enable iconv)
		$(use_enable static-libs static)
		--with-docdir=/usr/share/doc/${PF}
		--with-develdocdir=/usr/share/doc/${PF}a
		--includedir=/usr/include/${PN}
	)
	autotools-multilib_src_configure
	dodir /usr/share/man/man3
}

src_install() {
	autotools-multilib_src_install

	#avoid collision with allegro (bug 409305)
	local my_f=""
	for my_f in $(find "${D}"/usr/share/man/man3 -name "key.3*") ; do
		mv "${my_f}" "${my_f/key/elektra-key}" || die
		elog "/usr/share/man/man3/$(basename "${my_f}") installed as $(basename "${my_f/key/elektra-key}")"
	done

	if ! use static-libs; then
		find "${D}" -name "*.a" -delete || die
	fi

	dodoc AUTHORS ChangeLog NEWS README TODO
}
