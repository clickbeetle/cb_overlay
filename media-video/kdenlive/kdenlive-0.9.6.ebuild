# Copyright 1999-2013 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: /var/cvsroot/gentoo-x86/media-video/kdenlive/kdenlive-0.9.6.ebuild,v 1.2 2013/05/30 12:14:42 kensington Exp $

EAPI=5
KDE_LINGUAS="bs ca ca@valencia cs da de el es et fi fr ga gl he hr hu it ja lt
nb nds nl pl pt pt_BR ro ru sk sl sv tr uk zh_CN zh_TW"
KDE_HANDBOOK="optional"
OPENGL_REQUIRED="always"
inherit kde4-base

DESCRIPTION="A non-linear video editing suite for KDE"
HOMEPAGE="http://www.kdenlive.org/"
SRC_URI="mirror://kde/stable/${PN}/${PV}/src/${P}.tar.bz2"

LICENSE="GPL-2"
SLOT="4"
KEYWORDS="~amd64 ~ppc ~x86 ~x86-linux"
IUSE="debug"

RDEPEND="dev-libs/qjson
	>=media-libs/mlt-0.8.6-r1[ffmpeg,sdl,xml,melt,qt4,kdenlive]
	virtual/ffmpeg[encode,sdl,X]"
DEPEND="${RDEPEND}"

DOCS=( AUTHORS ChangeLog README TODO )