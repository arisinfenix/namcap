#
# namcap rules - unquoteddirvars
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

import re
from Namcap.ruleclass import *

class package(PkgbuildRule):
	name = "unquoteddirvars"
	description = "Looks for unquoted $pkgdir and $srcdir"
	def analyze(self, pkginfo, pkgbuild):
		needles = ['$pkgdir', '${pkgdir}', '$srcdir', '${srcdir}']
		hits = set()
		for line in pkginfo.pkgbuild:
			if not any(n in line for n in needles):
				continue
			double_quoted_strings = re.findall('"([^"]*)"', line)
			for n in needles:
				if line.count(n) != sum(n in s for s in double_quoted_strings):
					hits.add(n)
		for i in hits:
			self.warnings.append(("unquoted-dirvar %s", i))

# vim: set ts=4 sw=4 noet:
