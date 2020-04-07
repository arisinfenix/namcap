#
# namcap tests - unquoteddirvars
# Copyright (C) 2020 Michael Straube <michael.straube@posteo.de>
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

from Namcap.tests.pkgbuild_test import PkgbuildTest
import Namcap.rules

class NamcapUnqoutedDirVarsTest(PkgbuildTest):
	pkgbuild = """
# Maintainer: Arch Linux <archlinux at example.com>
# Contributor: Arch Linux <archlinux at example.com>

pkgname=mypackage
pkgver=1.0
pkgrel=1
pkgdesc="A package"
url="http://www.example.com/"
arch=('x86_64')
depends=('glibc')
license=('GPL')
options=('!libtool')
source=(ftp://ftp.example.com/pub/mypackage-0.1.tar.gz)
md5sums=('abcdefabcdef12345678901234567890')

build() {
  cd $srcdir/$pkgname-$pkgver
}

package() {
  make install DESTDIR=$pkgdir/
  install -Dm644 ${srcdir}/LICENSE ${pkgdir}/usr/share/licenses/${pkgname}
  install -Dm644 "${srcdir}/example.desktop" "$pkgdir"/usr/share/applications
}
"""
	test_valid = PkgbuildTest.valid_tests

	def preSetUp(self):
		self.rule = Namcap.rules.unquoteddirvars.package

	def test_example(self):
		needles = ['$pkgdir', '${pkgdir}', '$srcdir', '${srcdir}']
		r = self.run_on_pkg(self.pkgbuild)
		self.assertEqual(r.errors, [])
		self.assertEqual(set(r.warnings),
			set(("unquoted-dirvar %s", i) for i in needles))
		self.assertEqual(r.infos, [])

# vim: set ts=4 sw=4 noet:
