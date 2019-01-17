# -*- coding: utf-8 -*-

# Omnitux - educational activities based upon multimedia elements
# Copyright (C) 2008 Olav_2 (olav.olav@yahoo.fr)
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

import  os,  re, xml.dom, xml.dom.minidom, codecs
from pygame.locals import *
			
import constants, common


def has_image_extension(filename) :
	# filter files with image extensions
	png = re.compile('\.png$', re.IGNORECASE)
	jpg = re.compile('\.jpg$', re.IGNORECASE)
	gif = re.compile('\.gif$', re.IGNORECASE)
	if ((png.search(filename) != None) or (jpg.search(filename) != None) or (gif.search(filename) != None)) :
		if (os.path.isfile(filename)) :
			return True
	return False



def getText(element, i18n_dict = None, lang = None):
	# returns the text inside an XML tag
	nodelist = element.childNodes

	rc = u""

	key = element.getAttribute("key")

	if (cmp(key, "") != 0) :

		if (i18n_dict != None) :
			
			rc = i18n_dict.get(lang, key)
	
		else :
			common.error("Got an element with an i18n key, but no dictionary is available")


	else :
		for node in nodelist:
			if node.nodeType == node.TEXT_NODE:
				nd = node.data
				# suppresses new line characters (\r\n)
				# suppresses tabs
				# suppresses spaces
				nd = nd.strip(u"\r\n\t ")
				rc = rc + nd


	return rc

def getFloat(element) :
	return float(getText(element))

def getInt(element) :
	return int(getText(element))

def getBool(attr_value) :

	attr_value = attr_value.lower()

	if (cmp(attr_value, "true") == 0) :
		return True
	else :
		return False


def get_box_with_units(xml_box) :
	#Transforms some xml of the form:
	#	<pos_x>   5 </pos_x> 
	#	<pos_y>  10 </pos_y>
	#	<width>  40 </width>
	#	<height> 70 </height>
	#into two tuples (pos_x, pos_y) and (width, height)
	
	pos_x_tag = xml_box.getElementsByTagName("pos_x")[0]
	pos_y_tag = xml_box.getElementsByTagName("pos_y")[0]

	pos = (getFloat(pos_x_tag), getFloat(pos_y_tag))
	
	# note that the pos_y_tag unit is ignored
	# it is assumed it is the same than the pos_x_tag unit
	if (cmp(pos_x_tag.getAttribute("unit"), "px") == 0) :
		pos_unit = "px" # pixels
	else :
		pos_unit = "pc" # percents


	width_tag = xml_box.getElementsByTagName("width")[0]
	height_tag = xml_box.getElementsByTagName("height")[0]

	size = (getFloat(width_tag), getFloat(height_tag))

	if (cmp(width_tag.getAttribute("unit"), "px") == 0) :
		size_unit = "px" # pixels
	else :
		size_unit = "pc" # percents	


	return (pos, pos_unit, size, size_unit) 


def get_box(xml_box) :
	# here units are ignored, all values are assumed to be percents

	(pos, foo, size, foo) = get_box_with_units(xml_box)

	return (pos, size)


def save_xml_file(file_name, xml_data) :


	folder = os.path.dirname(file_name)

	if (not os.path.exists(folder)) :
		os.makedirs(folder)


	xml_file_handle = codecs.open(file_name, "w", "UTF8")

	xml_data.writexml(xml_file_handle, u"", u"\t", u"\n")

	xml_file_handle.close()	

	xml_data.unlink()
	
