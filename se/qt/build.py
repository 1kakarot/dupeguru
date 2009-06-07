#!/usr/bin/env python
# Unit Name: build
# Created By: Virgil Dupras
# Created On: 2009-05-24
# $Id$
# Copyright 2009 Hardcoded Software (http://www.hardcoded.net)

# On Windows, PyInstaller is used to build an exe (py2exe creates a very bad looking icon
# The release version is outdated. Use at least r672 on http://svn.pyinstaller.org/trunk

import os
import os.path as op
import shutil
from app import DupeGuru

def print_and_do(cmd):
    print cmd
    os.system(cmd)

# Removing build and dist
if op.exists('build'):
    shutil.rmtree('build')
if op.exists('dist'):
    shutil.rmtree('dist')

version = DupeGuru.VERSION
versioncomma = version.replace('.', ', ') + ', 0'
verinfo = open('verinfo').read()
verinfo = verinfo.replace('$versioncomma', versioncomma).replace('$version', version)
fp = open('verinfo_tmp', 'w')
fp.write(verinfo)
fp.close()
print_and_do("python C:\\Python26\\pyinstaller\\Build.py dgse.spec")
os.remove('verinfo_tmp')

print_and_do("xcopy /Y C:\\src\\vs_comp\\msvcrt dist")
print_and_do("xcopy /Y /S /I help\\dupeguru_help dist\\help")

aicom = '"\\Program Files\\Caphyon\\Advanced Installer\\AdvancedInstaller.com"'
shutil.copy('installer.aip', 'installer_tmp.aip') # this is so we don'a have to re-commit installer.aip at every version change
print_and_do('%s /edit installer_tmp.aip /SetVersion %s' % (aicom, version))
print_and_do('%s /build installer_tmp.aip -force' % aicom)
os.remove('installer_tmp.aip')