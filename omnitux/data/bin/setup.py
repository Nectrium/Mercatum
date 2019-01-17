# -*- coding: utf-8 -*-

# Omnitux - educational activities based upon multimedia elements
# Copyright (C) 2009 Olav_2 (olav.olav@yahoo.fr)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>


# instructions :

### change version in bin/constants.py ###

### change version in README.txt and in website ###

### update the change log in README.txt ###

### change version in tools/packaging/deb/control_install ! ###
### also in tools/packaging/rpm/omnitux_Fedora.spec ###
### and tools/packaging/rpm/omnitux_openSUSE.spec ###

# refresh author lists (on LICENSE.txt and on website)





# Works with python 2.5.4, pygame 1.7.1, py2exe 0.6.9 - py2.5, 
#
# from http://www.pygtk.org :
# pycairo 1.4.12-2 - py2.5, pygobject 2.14.2-2 - py2.5, pygtk 2.12.1-3 - py2.5
# gtk+ bundle 2.14.7-20090119 
#
# from http://ftp.gnome.org/pub/GNOME/binaries/win32 : (should be unpacjed in gtk folder)
# libbzip2 1.0.2
# libcroco 0.6.1
# libgsf 1.14.8
# libiconv 1.9.1
# librsvg 2.22.3-1
# libxml2 2.6.27
# svg-gdk-pixbuf-loader 2.22.3-1
# svg-gtk-engine 2.22.3-1


from distutils.core import setup
import py2exe

setup(
    windows = [
        {
            "script": "menu.py",
            "icon_resources": [(1, "..\\data\\default\\icons\\ico\\Omnitux.ico")]
        }
    ],
      author="Olav_2",
      author_email="olav_2 at users.sourceforge.net",
      url="http://omnitux.sourceforge.net/",

    options = {
                  'py2exe': {
                      'packages':'encodings',
                      'includes': 'cairo, pango, pangocairo, atk, gobject'
#, pygame.locals, pygame.mixer, pygame.mixer_music, pygame.font'
			#,
			#'bundle_files': 2 
                  }
              },

    )

# in gtk/etc/gtk-2.0/gdk-pixbufs.loaders, add :
#"c:/devel/target/5e32e6f9bd779a13110a7c6ff9016d6e/lib/gtk-2.0/2.10.0/loaders/svg_loader.dll"
#"svg" 2 "gtk20" "Scalable Vector Graphics" "LGPL"
#"image/svg" ""
#"svg" ""
#" <svg" "*    " 100
#" <!DOCTYPE svg" "*           " 100


# to build (in omnitux\bin):
# python setup.py py2exe

# suppress the "build" folder
# then move the "dist" folder upwards

# then :
# copy folders etc, lib and share from GTK to dist
# copy all the dlls from GTK/bin to dist (SVG support)

# copy bin/tagdefs.xml and bin/release to dist


# build the install with HM NIS Edit

##
# "new script from wizard"

# Application name = Omnitux
# version = X.Y
# publisher = ""
# Application website = http://omnitux.sourceforge.net/

# setup icon = {PATH}\omnitux\data\default\icons\ico\Omnitux.ico
# setup file = omnitux-X.Y.Z.win32.exe
# setup lang = English. French, German, Italian, Polish, Portuguese, Spanish
# GUI = Modern
# Compress = LZMA

# Application default directory = $PROGRAMFILES\Omnitux-VERSION
# allow user to change = yes
# License file = {PATH}\omnitux\LICENSE.txt
# Classic button

# Application files
# remove the examples
# add all the files im {PATH}\omnitux (just one MainSection)

# Application icons : unchanged

# Execute after setup :
# Program : None
# Readme : None

# use uninstaller: yes / default

# compile !



### build Linux version ###

# tar --exclude=.* --exclude=website  --exclude=tools --exclude-vcs -cvf  omnitux-X.Y.Z.noarch.tar omnitux

# bzip2 omnitux-X.Y.Z.noarch.tar

# upload file:

# eventually create folder on the FRS

# rsync -avP -e ssh omnitux-X.Y.Z.noarch.tar.bz2 olav_2,omnitux@frs.sourceforge.net:/home/pfs/project/o/om/omnitux/omnitux/vXXXX



### build package for Debian Ubuntu ###

# cd omnitux/tools/packaging/deb

# cd /tmp

# mv package.deb to distribution location




