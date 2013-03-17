# Copyright 1999-2012 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: /var/cvsroot/gentoo-x86/sys-auth/pambase/pambase-20150417.ebuild,v 1.1 2012/04/17 08:34:51 phajdan.jr Exp $

EAPI=4

inherit eutils pam

DESCRIPTION="PAM base configuration files"
HOMEPAGE="http://www.gentoo.org/proj/en/base/pam/"
SRC_URI="http://github.com/clickbeetle/cb-pambase/archive/${P}.tar.gz"
LICENSE="GPL-2"
SLOT="0"
IUSE="debug cracklib passwdqc consolekit gnome-keyring selinux mktemp pam_ssh +sha512 pam_krb5 minimal ldaplogin"
RESTRICT="binchecks"

RDEPEND="
	|| (
		>=sys-libs/pam-0.99.9.0-r1
		( sys-auth/openpam
		  || ( sys-freebsd/freebsd-pam-modules sys-netbsd/netbsd-pam-modules )
		)
	)
	cracklib? ( >=sys-libs/pam-0.99[cracklib] )
	consolekit? ( >=sys-auth/consolekit-0.3[pam] )
	gnome-keyring? ( >=gnome-base/gnome-keyring-2.20[pam] )
	selinux? ( >=sys-libs/pam-0.99[selinux] )
	passwdqc? ( >=sys-auth/pam_passwdqc-1.0.4 )
	mktemp? ( sys-auth/pam_mktemp )
	pam_ssh? ( sys-auth/pam_ssh )
	sha512? ( >=sys-libs/pam-1.0.1 )
	pam_krb5? (
		>=sys-libs/pam-1.1.0
		>=sys-auth/pam_krb5-4.3
	)
	ldaplogin? (
		sys-auth/pam_ldap
		sys-auth/nss_ldap
	)
	!<sys-freebsd/freebsd-pam-modules-6.2-r1
	!<sys-libs/pam-0.99.9.0-r1"
DEPEND="app-portage/portage-utils"

KEYWORDS="amd64"
S="${WORKDIR}/cb-pambase-${P}"
src_compile() {
	local implementation=
	local linux_pam_version=
	if has_version sys-libs/pam; then
		implementation="linux-pam"
		local ver_str=$(qatom `best_version sys-libs/pam` | cut -d ' ' -f 3)
		linux_pam_version=$(printf "0x%02x%02x%02x" ${ver_str//\./ })
	elif has_version sys-auth/openpam; then
		implementation="openpam"
	else
		die "PAM implementation not identified"
	fi

	use_var() {
		local varname=$(echo $1 | tr [a-z] [A-Z])
		local usename=${2-$(echo $1 | tr [A-Z] [a-z])}
		local varvalue=$(use $usename && echo yes || echo no)
		echo "${varname}=${varvalue}"
	}

	emake \
		GIT=true \
		$(use_var debug) \
		$(use_var cracklib) \
		$(use_var passwdqc) \
		$(use_var consolekit) \
		$(use_var GNOME_KEYRING gnome-keyring) \
		$(use_var selinux) \
		$(use_var mktemp) \
		$(use_var PAM_SSH pam_ssh) \
		$(use_var sha512) \
		$(use_var KRB5 pam_krb5) \
		$(use_var minimal) \
		IMPLEMENTATION=${implementation} \
		LINUX_PAM_VERSION=${linux_pam_version}
}

src_install() {
	emake GIT=true DESTDIR="${ED}" install
	if use ldaplogin; then
		dopamd "${FILESDIR}/system-auth.cb_allow_ldap"
	fi
}

pkg_postinst() {
	if use sha512; then
		elog "Starting from version 20080801, pambase optionally enables"
		elog "SHA512-hashed passwords. For this to work, you need sys-libs/pam-1.0.1"
		elog "built against sys-libs/glibc-2.7 or later."
		elog "If you don't have support for this, it will automatically fallback"
		elog "to MD5-hashed passwords, just like before."
		elog
		elog "Please note that the change only affects the newly-changed passwords"
		elog "and that SHA512-hashed passwords will not work on earlier versions"
		elog "of glibc or Linux-PAM."
	fi
}