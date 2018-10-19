#!/usr/bin/env python
# coding: utf-8

from __future__ import print_function


import re
import sys
from distutils import core, log

import os
import io


__version__ = os.getenv('VERSION', default=os.getenv('PVR', default='9999'))

cwd = os.getcwd()

# establish the eprefix, initially set so eprefixify can
# set it on install
EPREFIX = "@GENTOO_PORTAGE_EPREFIX@"

# check and set it if it wasn't
if "GENTOO_PORTAGE_EPREFIX" in EPREFIX:
    EPREFIX = ''


# Python files that need `version = ""` subbed, relative to this dir:
python_scripts = [os.path.join(cwd, path) for path in (
	'ganglia/version.py',
)]

class set_version(core.Command):
	"""Set python version to our __version__."""
	description = "hardcode scripts' version using VERSION from environment"
	user_options = []  # [(long_name, short_name, desc),]

	def initialize_options (self):
		pass

	def finalize_options (self):
		pass

	def run(self):
		ver = 'git' if __version__ == '9999' else __version__
		print("Setting version to %s" % ver)
		def sub(files, pattern):
			for f in files:
				updated_file = []
				with io.open(f, 'r', 1, 'utf_8') as s:
					for line in s:
						newline = re.sub(pattern, '"%s"' % ver, line, 1)
						if newline != line:
							log.info("%s: %s" % (f, newline))
						updated_file.append(newline)
				with io.open(f, 'w', 1, 'utf_8') as s:
					s.writelines(updated_file)
		quote = r'[\'"]{1}'
		python_re = r'(?<=^version = )' + quote + '[^\'"]*' + quote
		sub(python_scripts, python_re)


core.setup(
	name='ganglia_api',
	version=__version__,
	description='API layer that exposes ganglia data in a RESTful JSON manner',
	author='satterly',
	author_email='',
	maintainer='Orchard Systems',
	maintainer_email='admin@orchardsystems.com',
	url='https://github.com/teamorchard/ganglia-api',
	packages=['ganglia_api'],
	python_requires='=2.7',
	cmdclass={
		'set_version': set_version,
	},
)

