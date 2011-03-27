# 
# namcap rules - pacman package interface
# Copyright (C) 2003-2009 Jason Chu <jason@archlinux.org>
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

import tarfile, os, re, subprocess
import sys
from Namcap.package import PacmanPackage

pacmandb = '/var/lib/pacman/local/'

for i in open('/etc/pacman.conf'):
	m = re.match('\s*DBPath\s*=\s*([\S^#]+)', i)
	if m != None:
		pacmandb = os.path.join(m.group(1), 'local/')
		break

def load(package, root=None):
	if root == None:
		root = pacmandb
	# We know it's a local package
	if os.path.isfile(package) and tarfile.is_tarfile(package):
		return None
	else:
		searchstr = re.compile('(.*)-([^-]*)-([^-]*)')
		for i in os.listdir(root):
			n = searchstr.match(i)
			if n == None:
				continue
			if n.group(1) == package:
				# We found the package!
				return loadfromdir(os.path.join(root, i))

		# Maybe it's a provides then...
		for i in os.listdir(root):
			prov = loadfromdir(os.path.join(root, i))

			if prov != None and 'provides' in prov and package in prov["provides"]:
				return prov

		return None

def loadfromdir(directory):
	"""Read package information from a directory in the database"""
	if not os.path.isdir(directory):
		return None

	data = ""
	for info in ('desc', 'depends', 'files'):
		path = os.path.join(directory, info)
		if os.path.isfile(path):
			dbfile = open(path, encoding="utf-8", errors="ignore")
			data += dbfile.read()
			dbfile.close()

	ret = PacmanPackage(db = data)
	return ret

def getprovides(provides):
	packagelist = []

	searchstr = re.compile('(.*)-([^-]*)-([^-]*)')
	for i in os.listdir(pacmandb):
		pac = loadfromdir(os.path.join(pacmandb, i))
		if 'provides' in pac and provides in pac["provides"]:
			packagelist.append(pac.name)

	return packagelist
# vim: set ts=4 sw=4 noet:
