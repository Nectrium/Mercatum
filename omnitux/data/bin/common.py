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

import pygame, sys, os, random, copy, datetime, string, xml.dom, xml.dom.minidom, traceback, getopt, codecs
from pygame.locals import *

import ui, constants, xml_funcs, i18n

def init() :

	info("Mixer pre init")
	pygame.mixer.pre_init(44100, -16, 2,  constants.mixer_buffersize)
	
	# Let's go !
	info("pygame init")
	(good,bad) = pygame.init()
	
	if (bad > 0) :
		warn("pygame.init problem, failed attempts")
		if (os.name == "nt") :
			# Windows system fallback, try standard driver instead direct X
			warn("trying with standard graphic driver instead of direct X")
			os.putenv("SDL_VIDEODRIVER", "windib")
			pygame.init()

	try:
		opts, args = getopt.getopt(sys.argv[1:], "w=:h=:ov", ["width=", "height=", "help", "force_light"])

	except getopt.GetoptError, err :

		print str(err) 
		
		error("Error while parsing command line arguments")
		error(str(err))

		sys.exit(2)


	globalvars = GlobalVars()

	for o, a in opts:

		if o == "-v":
			# TODO
			# To implement
			info("Command line parameter : verbose mode On")


		elif o in ("-h", "--help"):
			print "Omnitux version " + constants.version
			print ""
			print "Usage :"
			print "\t omnitux.sh [--width=globalvars.screen_width] [--height=globalvars.screen_height] [-v verbose] [--force_light]"
			print
			print "force_light = force use of '.light' media files instead of high quality files"
			print

			sys.exit()

		elif o in ("-w", "--width") :
			globalvars.screen_width = int(a)

			info("User requested width " + a)

		elif o in ("-h", "--height") :
			globalvars.screen_height = int(a)

			info("User requested height " + a)

		elif (cmp(o, "--force_light") == 0) :

			info("Forcing 'light' mode")

			globalvars.force_light = True

		else:
			print " unhandled option : " + o

	# initialisation : screen display 

	try :

		info("Trying to switch to fullscreen")

		if ((globalvars.screen_width == 0) or (globalvars.screen_height == 0)) :
			info("No user parameters => using current desktop resolution")
			(globalvars.screen_width, globalvars.screen_height) = (0,0)

		screen = pygame.display.set_mode((globalvars.screen_width, globalvars.screen_height), FULLSCREEN)

		info("Success for opening in fullscreen")

	except :
		warn("Could not use desktop resolution or user choosen resolution")
		warn("This might be caused by an old SDL version")

		info("Looking for all available display modes")
		screen_modes = pygame.display.list_modes(0, pygame.FULLSCREEN)
		
		if ((globalvars.screen_width == 0) or (globalvars.screen_height == 0)) :
			info("No user paramaters => biggest dimensions for the screen")
			(globalvars.screen_width, globalvars.screen_height) = screen_modes[0]

		info("Opening the fullscreen")
		screen = pygame.display.set_mode((globalvars.screen_width, globalvars.screen_height), FULLSCREEN)	

	# hide the system mouse cursor
	transparent_mouse_cursor()

	globalvars.screen = screen

	return globalvars


def get_user_lang() :

	import locale

	# Trying to guess the main language of the user
	(lang_var, foo) = locale.getdefaultlocale()

	user_country = None

	if (lang_var != None) :

		lang_var = lang_var.lower()

		if (len(lang_var) >= 2) :
			lang_var_small = lang_var[0:2]

			if (len(lang_var) > 3) :
				user_country = lang_var[3:len(lang_var)]

		else :
			lang_var_small = lang_var


		if (lang_var_small in constants.supported_languages) :
			default_language = lang_var_small
		else :
			default_language = "en"

	else :
		default_language = "en"


	return (default_language, user_country)


class GlobalVars() :

	# This class handles global variables (setup, ...)

	def __init__(self) :

		# default values

		self.music_on = True

		self.screen = None

		self.fonts = None

		self.force_light = False

		self.main_language_mode = "system"
		(self.main_language, self.user_country) = get_user_lang()
	
		self.active_languages = copy.copy(constants.supported_languages)


		self.release = "unknown"

		self.screen_width = 0
		self.screen_height = 0

		self.music_volume = constants.music_volume

		self.congrats_sounds_active = True

		self.congrats_voices_active = True

		self.display_igloo = True

		self.arcade_mode = False
		

		self.highscore = True

		# trying to load options file if available

		user_options_file = os.path.join(constants.home_dir, constants.user_options_filename)

		if (os.path.isfile(user_options_file)) :

			try :


				xml_data = xml.dom.minidom.parse(user_options_file)


				# load screen resolution

				screen_resolution_nodes = xml_data.getElementsByTagName("screen_resolution")

				if (len(screen_resolution_nodes) > 0) :
					
					screen_width_nodes = screen_resolution_nodes[0].getElementsByTagName("width")
					screen_height_nodes = screen_resolution_nodes[0].getElementsByTagName("height")

					if ((len(screen_width_nodes) > 0) and (len(screen_height_nodes) > 0)) :

						width = xml_funcs.getFloat(screen_width_nodes[0])
						height = xml_funcs.getFloat(screen_height_nodes[0])

						if ((width, height) in pygame.display.list_modes()) :
							self.screen_width = width
							self.screen_height = height

				# load music volume

				music_volume_nodes = xml_data.getElementsByTagName("music_volume")

				if (len(music_volume_nodes) > 0) :

					user_music_volume = xml_funcs.getFloat(music_volume_nodes[0])

					if ((user_music_volume >= 0) and (user_music_volume <= 1)) :
						self.music_volume = user_music_volume

				# load congratulation sounds mode

				congrat_sound_nodes = xml_data.getElementsByTagName("congrats_sounds")

				if (len(congrat_sound_nodes) > 0) :
					
					self.congrats_sounds_active = xml_funcs.getBool(congrat_sound_nodes[0].getAttribute("active"))
				else :
					self.congrats_sounds_active = True


				# load congratulation voices mode

				congrat_voices_nodes = xml_data.getElementsByTagName("congrats_voices")

				if (len(congrat_voices_nodes) > 0) :
					
					self.congrats_voices_active = xml_funcs.getBool(congrat_voices_nodes[0].getAttribute("active"))
				else :
					self.congrats_voices_active = True


				# load display igloo mode

				igloo_nodes = xml_data.getElementsByTagName("igloo")

				if (len(igloo_nodes) > 0) :
					
					self.display_igloo = xml_funcs.getBool(igloo_nodes[0].getAttribute("display"))


				# load arcade mode

				arcade_nodes = xml_data.getElementsByTagName("arcade")

				if (len(arcade_nodes) > 0) :
					
					self.arcade_mode = xml_funcs.getBool(arcade_nodes[0].getAttribute("enabled"))



				# load default language

				language_nodes = xml_data.getElementsByTagName("language")
				
				if (len(language_nodes) > 0) :

					main_language = language_nodes[0].getAttribute("default")

					if (cmp(main_language, "system") != 0) :

						self.main_language = main_language
						self.main_language_mode = "user"
						



			except Exception, e :
				error("Can not load user options file ", e, traceback.format_exc())


		# trying to identify the release type (development, complete, light)
		try :
			release_handler = open(constants.release_file, "r")

			self.release = release_handler.read().rstrip('\n')

			release_handler.close()

		except Exception, e :
			error("Can not get release info ", e, traceback.format_exc())


		self.screen_width = int(self.screen_width)
		self.screen_height = int(self.screen_height)


	def save_user_options(self) :

		try :
			user_options_file = os.path.join(constants.home_dir, constants.user_options_filename)

			impl = xml.dom.getDOMImplementation()
	
			xml_data = impl.createDocument(constants.namespace, u"omnitux_user_options", None)

			root_node = xml_data.documentElement

			root_node.setAttribute(u"Version", constants.version)


			# save screen resolution

			resolution_node = xml_data.createElement("screen_resolution")

			width_node = xml_data.createElement("width") 

			width_node.appendChild(xml_data.createTextNode(str(self.screen_width)))

			resolution_node.appendChild(width_node)

			height_node = xml_data.createElement("height") 

			height_node.appendChild(xml_data.createTextNode(str(self.screen_height)))

			resolution_node.appendChild(height_node)

			root_node.appendChild(resolution_node)


			# save music volume

			music_volume_node = xml_data.createElement("music_volume")

			music_volume_node.appendChild(xml_data.createTextNode(str(self.music_volume)))

			root_node.appendChild(music_volume_node)


			# save congratulation sounds mode

			congrat_sounds_node = xml_data.createElement("congrats_sounds")

			congrat_sounds_node.setAttributeNode(xml_data.createAttribute("active"))

			congrat_sounds_node.setAttribute("active", str(self.congrats_sounds_active))

			root_node.appendChild(congrat_sounds_node)


			# save congratulation voices mode

			congrat_voices_node = xml_data.createElement("congrats_voices")

			congrat_voices_node.setAttributeNode(xml_data.createAttribute("active"))

			congrat_voices_node.setAttribute("active", str(self.congrats_voices_active))

			root_node.appendChild(congrat_voices_node)


			# save igloo display mode

			igloo_node = xml_data.createElement("igloo")

			igloo_node.setAttributeNode(xml_data.createAttribute("display"))

			igloo_node.setAttribute("display", str(self.display_igloo))

			root_node.appendChild(igloo_node)


			# save arcade mode

			arcade_node = xml_data.createElement("arcade")

			arcade_node.setAttributeNode(xml_data.createAttribute("enabled"))

			arcade_node.setAttribute("enabled", str(self.arcade_mode))

			root_node.appendChild(arcade_node)


			# save default language

			language_node = xml_data.createElement("language")
				
			language_node.setAttributeNode(xml_data.createAttribute("default"))

			if (cmp(self.main_language_mode, "system") == 0) :
				default_language = "system"

			else :
				default_language = self.main_language

			language_node.setAttribute("default", default_language)


			root_node.appendChild(language_node)



			# write the file

			xml_funcs.save_xml_file(user_options_file, xml_data)

		except Exception, e :
			error("Could not save user options file ", e, traceback.format_exc())







def load_tag_defs() :
	info("Loading tag definitions")

	tag_defs = []


	try :
		xml_data = xml.dom.minidom.parse(constants.tag_defs_filename)

		xml_omnitux_tag_defs_node = xml_data.getElementsByTagName("omnitux_tag_defs")[0]

		xml_tag_def_nodes = xml_omnitux_tag_defs_node.getElementsByTagName("tag_def")

		info("Header structure looks ok")

		for xml_tag_def_node in xml_tag_def_nodes :
			
			tag_node = xml_tag_def_node.getElementsByTagName("tag")[0]

			image_node = xml_tag_def_node.getElementsByTagName("image")[0]

			text_nodes = xml_tag_def_node.getElementsByTagName("text")

			tag = xml_funcs.getText(tag_node)
			image_filename = xml_funcs.getText(image_node)

			tag_def = Tag_def(tag, image_filename)

			for text_node in text_nodes :
				text = xml_funcs.getText(text_node)
				language = text_node.getAttribute("lang")

				tag_def.append_text(text, language)


			tag_defs.append(tag_def)

		
		return tag_defs

	except Exception, e :
		error("Impossible to read the contents of "+constants.tag_defs_filename)
		error("File format might be incorrect")
		error("Exception follow ", e, traceback.format_exc())

		raise BadXMLException()


class Tag_def() :
	
	def __init__(self, tag, image_filename) :
		self.tag = tag
		self.image_filename = image_filename

		self.texts = {}

	def append_text(self, text, lang) :
		self.texts[lang] = text

	def get_text(self, lang) :
		text = None

		text = i18n.get_text_from_dict(self.texts, lang)


		return text



def info(info, exception = None) :
	write_log("INFO", info, exception, None)

def warn(warning, exception = None) :
	write_log("WARN", warning, exception, None)
	
def error(error, exception = None, trace = None) :
	write_log("ERROR", error, exception, trace)
	
	
def write_log(type_of_log, text, exception, trace) :

	now = datetime.datetime.now()

	line_start = now.isoformat(" ") + '\t' + type_of_log + '\t'

	to_write = line_start + text + '\n'

	print to_write
	
	if (exception != None) :
		
		#(exc_type, exc_value, exc_traceback) = sys.exc_info()

		#to_write = line_start + exc_value + '\n'
		#f.write(to_write)	
		
		to_write = line_start + unicode(exception) + '\n'
		print to_write
		
		if (trace != None) :
			to_write = line_start + unicode(trace) + "\n"
		
			print unicode(to_write)
	
	return		


def transparent_mouse_cursor() :

	# for some weird reason
	# pygame.mouse.set_visible(False)
	# makes the mouse "slow"
	# so it is better to fake it with a totally
	# transparent mouse

	(data, mask) = pygame.cursors.compile(("        ","        ","        ","        ","        ","        ","        ","        "))

	pygame.mouse.set_cursor((8,8), (0, 0), data, mask)




def start_music(files = constants.default_music_files, globalvars = None) :

	info("Starting music")
	
	if (len(files) > 0) :
		music_index = random.randint(0, len(files)-1)
		
		music_file = find_file(files[music_index], globalvars)
		
		try :
			pygame.mixer.music.load(music_file)
			# play the tune once

			pygame.mixer.music.play(0 ,0.0)
			# set an endevent for the next one
			pygame.mixer.music.set_endevent(constants.ENDMUSICEVENT)
			
			pygame.mixer.music.set_volume(globalvars.music_volume)

			info("Now playing music : "+music_file)

		except Exception, e :
			error("Unable to play music.", e, traceback.format_exc())	


	else :
		warn("No music file to play")

def stop_music() :

	info("Stopping music")
	pygame.mixer.music.stop()


def get_files(path, extensions) :
	
	path = find_folder(path)
	
	# filter files with given extensions (list, without dots)
	# returns found_files	
	found_files = []
	
	entries = os.listdir(path)
	entries_with_path = []
	
	for entry in entries :	
		entry = os.path.join(path, entry)
		entries_with_path.append(entry)
	
	subfolders = filter(os.path.isdir, entries_with_path)		
	files = filter(os.path.isfile, entries_with_path)

	for file in files :
		
		(before, foo, extension) = file.rpartition(".")
				
		if (extension in extensions) :
			found_files.append(file)

	for subfolder in subfolders :
		more_found_files = get_files(subfolder, extensions)

		for found_file in more_found_files :
			found_files.append(found_file)
			
	return found_files
	


def randomize_rects(components) :
	# the purpose of this function is to shuffle a list of components
	# Example : messing up puzzle elements
	
	# the list "components" given as a parameter is directly modified
	index_component = 0
	
	rects = []
	
	for component in components :
		rect = copy.copy(component.rect)
		rects.append(rect)
		
	
	while (len(rects) > 0) :
		
		random_index = random.randint(0, len(rects)-1)
		
		components[index_component].rect = rects[random_index]
		
		rects.remove(rects[random_index])
		
		index_component = index_component + 1

def randomize_list(ar) :
	# the purpose of this function is to shuffle the elements of a list
	
	# the list given as a parameter is directly modified
	index_array = 0

	array_new = []

	
	while (len(ar) > 0) :
		
		random_index = random.randint(0, len(ar)-1)
		
		array_new.append(ar[random_index])
		
		del ar[random_index]
		
	return array_new


def center_vert_absolute(items, y_pos, height) :
	# vertically centers some ui components after the absolute position y_pos
	# inside a rectangle of height pixels
	
	min_y = y_pos+height
	max_y = y_pos
	
	for item in items :
		cur_min_y = item.rect.top
		cur_max_y = item.rect.bottom
		
		if (cur_min_y < min_y) :
			min_y = cur_min_y
		
		if (cur_max_y > max_y) :
			max_y = cur_max_y
	
	
	if ((min_y >= y_pos) and (max_y <= y_pos + height)) :
		
		delta_y = (height - (max_y - min_y)) // 2
		

		if (delta_y > 0) :
			
			for item in items :
				
				item.rect.top = item.rect.top + delta_y
			

class Game_set() :
	# a set of games contained inside an XML file
	# single activity files do not need to use a "games" XML tag
	def __init__(self, globalvars, xml_filename) :

		self.globalvars = globalvars

		self.levels = []

		self.xml_filename = xml_filename

		self.languages = []

		self.titles = {}
		self.thumb = None

		self.tags = []

		self.game_set_node = None


		try :
			self.xml_data = xml.dom.minidom.parse(xml_filename)

			# info("Loading file " + xml_filename)

		except :
			error("Impossible to read the contents of "+xml_filename)
			error("File format might be incorrect")

			raise BadXMLException()

		# trying to load an i18n dictionary
		self.i18n_dict = i18n.i18n_dict(self.xml_data)

		self.xml_game_set_nodes = self.xml_data.getElementsByTagName("game_set")

		if (len(self.xml_game_set_nodes) > 0) :
			# we enter there if the file is a game_set
			self.game_set_node = self.xml_game_set_nodes[0]

			# get the title of the game_set in different languages
			title_nodes = self.game_set_node.getElementsByTagName("title")
			
			for title_node in title_nodes :
				if (title_node.parentNode == self.game_set_node) :

					title = xml_funcs.getText(title_node)
					language = title_node.getAttribute("lang")
					
					self.languages.append(language)
					self.titles[language] = title

			# eventual thumbnail
			thumb_nodes = self.game_set_node.getElementsByTagName("thumbnail")
		
			if (len(thumb_nodes) > 0) :
				self.thumb = xml_funcs.getText(thumb_nodes[0])

			# amount of game rounds (applies by default to all levels)
			self.rounds_amount_nodes = self.game_set_node.getElementsByTagName("rounds")
			if (len(self.rounds_amount_nodes) > 0) :
				if (self.rounds_amount_nodes[0].parentNode == self.game_set_node) :
					self.game_rounds_amount = xml_funcs.getInt(self.rounds_amount_nodes[0])
				else :
					self.game_rounds_amount = constants.infinite
			else :
				self.game_rounds_amount = constants.infinite

		else :
			# we're here if the file was only made of a 'game' and not a 'game_set'
			self.game_rounds_amount = 1

			# we 'fake', the game node is considered a game_set
			self.game_set_node = self.xml_data


		self.xml_level_nodes = self.game_set_node.getElementsByTagName("level")

		if (len(self.xml_level_nodes) == 0) :
			# no level defined, so we let the game_set act like a level
			level = Level(self.globalvars, self.game_set_node, self)
			self.levels.append(level)

		else :

			for xml_level_node in self.xml_level_nodes :
				level = Level(self.globalvars, xml_level_node, self)
				self.levels.append(level)



		# TODO allow multiple types games
		self.game_type = self.levels[0].games[0].game_type



		# TODO put real tags

		xml_tag_nodes = self.game_set_node.getElementsByTagName("tag")

		if (len(xml_tag_nodes) > 0) :
			for xml_tag_node in xml_tag_nodes :
				tag = xml_funcs.getText(xml_tag_node).lower()
				self.tags.append(tag)

		else :
			# if no tags defined, the game type becomes a tag
			self.tags = [self.levels[0].games[0].game_type]



		# get the indexes for sorting in menu

		self.menu_index = {}

		menu_index_nodes = self.game_set_node.getElementsByTagName("menu_index")

		self.max_menu_index_len = 1

		if (len(menu_index_nodes) > 0) :
			for menu_index_node in menu_index_nodes :

				lang = menu_index_node.getAttribute("lang")
				value = menu_index_node.getAttribute("value")

				if (cmp(lang, "") != 0) :
					self.menu_index[lang] = value
				else :
					for lang in constants.supported_languages :
						if (lang not in self.menu_index.keys()) :

							self.menu_index[lang] = value

				if (len(value) > self.max_menu_index_len) :
					self.max_menu_index_len = len(value)



	def get_title(self, lang) :

		title = None

		if (lang in self.titles) :
			title = i18n.get_text_from_dict(self.titles, lang)

		if (title == None) :
			if (lang in self.levels[0].games[0].titles) :
				title = self.levels[0].games[0].get_title(lang)

		return title

	def get_menu_index(self, lang) :
		
		# function to get a number to sort the activities in the menu
		# the value returned might differ depending on the language

		try :
			value = self.menu_index[lang]

		except KeyError :

			value = " "

		value = string.ljust(value, self.max_menu_index_len, " ")

		return value


	def get_author(self) :

		# TODO : allow multiple authors and look for authors elsewhere !
	
		author = ""

		if (len(self.xml_game_set_nodes) > 0) :
			author = self.xml_game_set_nodes[0].getAttribute("author")

		if (cmp(author, "") == 0) :
			author = self.levels[0].games[0].author

		return author


	def get_tags(self) :

		return self.tags


	def get_thumb(self) :
		if (self.thumb == None) :
			return self.levels[0].games[0].thumb
		else :
			return self.thumb
		
class Level() :
	# a difficulty level contains one or more games

	# TODO : allow different rounds amount depending on level

	def __init__(self, globalvars, xml_level_node, game_set) :

		self.globalvars = globalvars

		self.games = []
		self.xml_level_node = xml_level_node

		self.game_set = game_set

		self.game_rounds_amount = self.game_set.game_rounds_amount

		try :
			self.difficulty = self.xml_level_node.getAttribute("difficulty")
		except Exception, e :
			# not clean...
			# we arrive here if the xml_level_node happens to be a game (faked level for backwards compatibility)
			self.difficulty = "1"


		# amount of game rounds for this particular level
		self.rounds_amount_nodes = self.xml_level_node.getElementsByTagName("rounds")
		if (len(self.rounds_amount_nodes) > 0) :
			if (self.rounds_amount_nodes[0].parentNode == self.xml_level_node) :
				# here, we override the game_rounds_amount value which came from the game_set
				# object
				self.game_rounds_amount = xml_funcs.getInt(self.rounds_amount_nodes[0])

		self.xml_game_nodes = self.xml_level_node.getElementsByTagName("game")


		if (len(self.xml_game_nodes) == 0) :
			error(" no game tag found")
			
			raise BadXMLException()

		for xml_game_node in self.xml_game_nodes :
			game = Game(self.globalvars, xml_game_node, self, None)
			self.games.append(game)

	def get_difficulty(self) :

		return self.difficulty

	def get_difficulty_level_image(self) :

		# TODO : manage the case of an unknown difficulty level code ?
		
		try :
			difficulty_level_image = constants.level_icons[self.difficulty]

		except Exception, e :
			warn("No icon for difficulty "+self.difficulty)	
			difficulty_level_image = constants.level_icons["1"]

		return difficulty_level_image


class Game() :
	# a single activity
	# game_type can be :
	# - associate
	# - puzzle
	# - memory cards
	def __init__(self, globalvars, xml_game_node, level, score = None) :

		self.globalvars = globalvars

		self.xml_game_node = xml_game_node
		self.level = level
		
		self.game_type = ""
		self.xml_file_version = ""
		self.languages = []
		self.i18n_dict = self.level.game_set.i18n_dict
		self.author = ""
		self.titles = {}
		self.thumb = None


		if (score != None) :
			self.score = score
		else :
			self.score = Score(globalvars)


		# TODO : implement custom music for a given game
		self.music_files = constants.default_music_files
	
		self.game_type = self.xml_game_node.getAttribute("type")

		
		
		self.xml_file_version = self.xml_game_node.getAttribute("xml_version")
		self.author = self.xml_game_node.getAttribute("author")
		
		title_nodes = self.xml_game_node.getElementsByTagName("title")

		if (len(title_nodes) == 0) :
			# no title found, we try to get it from the game_set above
			title_nodes = self.xml_game_node.parentNode.getElementsByTagName("title")

			if (len(title_nodes) == 0) :
				# yet no title ? we are probably inside a level tag
				# so let's go up again
				title_nodes = self.xml_game_node.parentNode.parentNode.getElementsByTagName("title")
		
		for title_node in title_nodes :
			title = xml_funcs.getText(title_node)
			language = title_node.getAttribute("lang")
			
			self.languages.append(language)
			self.titles[language] = title
		
		# eventual thumbnail
		thumb_nodes = self.xml_game_node.getElementsByTagName("thumbnail")
		
		if (len(thumb_nodes) > 0) :
			self.thumb = xml_funcs.getText(thumb_nodes[0])
		
		background_nodes = self.xml_game_node.getElementsByTagName("background")
		
		self.backgrounds = []
		for background_node in background_nodes :

			background_file = xml_funcs.getText(background_node)
			
			background_mode = background_node.getAttribute("mode")

			if (background_mode == "") :
				# by default, the background will be stretched to fill all the screen
				background_mode = "FILL"

			self.backgrounds.append((background_file, background_mode))


		music_nodes = self.xml_game_node.getElementsByTagName("music")
		if (len(music_nodes) > 0) :
			# Only the first node is taken into account
			music_node = music_nodes[0]
			
			self.music_mode = music_node.getAttribute("mode")
			
			self.music_files = []
			
			music_files = music_node.getElementsByTagName("file")
			for music_file in music_files :
				self.music_files.append(music_files)
			
			if (len(self.music_files) == 0) :
				self.music_files = constants.default_music_files
			
		else :
			self.music_mode = "on"
			self.music_files = constants.default_music_files


		self.rounds_amount = self.xml_game_node.getElementsByTagName("rounds")
		if (len(self.rounds_amount) > 0) :
			self.rounds_amount = xml_funcs.getInt(self.rounds_amount[0])
		else :
			self.rounds_amount = constants.infinite
			
		self.rounds_done = 0

			
	def get_title(self, lang) :
		return i18n.get_text_from_dict(self.titles, lang)



	def start_timer(self) :
		if (self.globalvars.arcade_mode == True) :
			self.score.timer.run()


	def stop_timer(self) :
		if (self.globalvars.arcade_mode == True) :
			self.score.timer.stop()


	
def light_name(file) :
	# inserts the "light" prefix before the file extension
	# for instance picture.jpg becomes picture.light.jpg
	
	# TODO : do not add the 'light' in case the file name already contains it !

	(file_with_no_extension, extension) = os.path.splitext(file)

	return (file_with_no_extension+".light"+extension)


def find_file(file, globalvars = None) :
	# the aim of this procedure is to find a file
	# in one of the user paths


	file_light = light_name(file)

	force_light = False
	if (globalvars != None) :
		force_light = globalvars.force_light
	


	if (os.path.isfile(file)) :

		if (force_light == True) :
			if (os.path.isfile(file_light)) :
				return file_light

		return file
	else :

		for path in constants.data_folders :
			test_file = os.path.join(path, file) 
			test_file_light = os.path.join(path, file_light) 

			if (os.path.isfile(test_file)) :
				
				if (force_light == True) :
					if (os.path.isfile(test_file_light)) :
						return test_file_light

				return test_file

			else :
				if (os.path.isfile(test_file_light)) :
					return test_file_light

			
	
	warn("File not found "+file)

	return "Not found"
	
def find_folder(folder) :
	# same idea than find_file
	
	if (os.path.isdir(folder)) :
		return folder
	else :
		# TODO add more paths to look for (home...)
		
		return os.path.join(constants.data_folders[0], folder)
		

class EndActivityException(Exception) :
	# an exception when someone quits an activity before finishing it

	def __str__(self) :
		return("User stopped the activity")
		
class BadXMLException(Exception) :
	# this exception is raised when Omnitux detects an incoherency
	# in the xml setup

	def __str__(self) :
		return("Bad XML setup.")


class Run_Screen() :
	def __init__(self, globalvars, game = None) :

		self.globalvars = globalvars
		self.screen = globalvars.screen
		self.main_language = globalvars.main_language

		info("Run_Screen Super class initialization")
		info("Language = " + self.main_language)

		self.running = True

		self.clock = pygame.time.Clock()

		self.mouse_clicked = False

		self.undrag = False

		self.game = game # by default, no activity is associated to the screen

		if (self.game != None) :

			if (cmp(self.game.music_mode, "off") == 0) :
				stop_music()


	def run_pre(self) :

		# list of standard stuff which has to be executed before screen specific behaviour

		self.dirty_rects = []

		# don't forget to initialise the variable self.current_page (in subclass) before running this !
		self.dirty_rects = self.dirty_rects + self.current_page.erase_sprites()

		if (self.undrag == True) : 
			self.dirty_rects = self.dirty_rects + self.current_page.undrag_sprite()  
			self.undrag = False 

		self.key_events = []


		# reading the user input events
		for event in pygame.event.get():

			if event.type == QUIT:
				self.running = False
			
			elif event.type == constants.ENDMUSICEVENT :
				if (self.game == None) :
					# if the screen is not related to a game, the music should loop
					start_music(constants.default_music_files, self.globalvars)	
				elif (cmp(self.game.music_mode, "off") != 0) :
					# if the screen is a game screen, we start music only if this is allowed by
					# the music_mode parameter
					start_music(self.game.music_files, self.globalvars)
				
			elif event.type == MOUSEBUTTONUP :
				self.mouse_clicked = False
				
				if (self.current_page.dragged_sprite != None) :
					self.undrag = True
			
			elif event.type == MOUSEBUTTONDOWN :
				self.mouse_clicked = True
				self.mouse_pos = event.pos
				self.mousebutton = event.button	
			
			elif event.type == KEYDOWN:

				if event.key == K_ESCAPE:
					self.running = False
					raise(EndActivityException())
					
				elif event.key == K_F1 :

					if (self.game != None) :
						if (cmp(self.game.music_mode, "off") == 0) :
							start_music(self.game.music_files, self.globalvars)
							self.game.music_mode = "on"
						else :
							stop_music()
							self.game.music_mode = "off"
						
						

				elif event.key == K_SCROLLOCK :
					
					info("Screen refresh requested")
					
					# TODO : enable again someday ?
					# this was messing mouse manipulation

					# self.current_page.draw()
					
					# pygame.display.flip()
					
				elif event.key == K_PRINT :
					
					info("Screenshot creation")

					date_time = datetime.datetime.now()
					file_name = os.path.join(constants.folder_log,"Omnitux_"+date_time.isoformat()+".png")
					pygame.image.save(self.screen,file_name)	

				elif event.key == K_PAUSE :

					# print resource usage statistics in the log

					try :
						# This should work only on UNIX like OSes
						# TODO : think about something similar for Windows ?
	
						import resource

						usage = resource.getrusage(resource.RUSAGE_SELF)

						info("perf - ru_maxrss - maximum resident set size - " + str(usage.ru_maxrss))
						info("perf - ru_ixrss - shared memory size - " + str(usage.ru_ixrss))
						info("perf - ru_idrss - unshared memory size - " + str(usage.ru_idrss))
						info("perf - ru_isrss - unshared stack size - " + str(usage.ru_isrss))
						info("perf - ru_minflt - page faults not requiring I/O - " + str(usage.ru_minflt))
						info("perf - ru_majflt - page faults requiring I/O - " + str(usage.ru_majflt))
						info("perf - ru_nswap - number of swap outs - " + str(usage.ru_nswap))
						info("perf - ru_inblock - block input operations - " + str(usage.ru_inblock))
						info("perf - ru_oublock - block output operations - " + str(usage.ru_oublock))
						info("perf - ru_msgsnd - messages sent - " + str(usage.ru_msgsnd))
						info("perf - ru_msgrcv - messages received - " + str(usage.ru_msgrcv))
						info("perf - ru_nsignals - signals received - " + str(usage.ru_nsignals))
						info("perf - ru_nvcsw - voluntary context switches - " + str(usage.ru_nvcsw))
						info("perf - ru_nivcsw - involuntary context switches - " + str(usage.ru_nivcsw))


					except Exception, e :
						error("Exception fired", e, traceback.format_exc())


				else :
					self.key_events.append(event)


	def run_post(self) :

		# list of standard stuff which has to be executed after screen specific behaviour

		if (self.game != None) :
			self.dirty_rects = self.dirty_rects + self.current_page.draw_arcade()

		self.dirty_rects = self.dirty_rects + self.current_page.draw_sprites() 
		
		pygame.display.update(self.dirty_rects)		
		
		self.clock.tick(constants.framerate)


	def set_music_volume(self, music_volume) :
		
		pygame.mixer.music.set_volume(music_volume)


class Score() :
	# class used to record good and/or wrong answers and/or time in arcade mode
	def __init__(self, globalvars) :

		self.globalvars = globalvars

		self.count_good = False
		self.count_wrong = False
		self.record_time = False


		# TODO : fix this default value
		self.name = "Test" # name of the player who owns the score
		self.datetime = None # highscore datetime = number of seconds since 1970

		self.good_answers = 0
		self.wrong_answers = 0

		self.timer = Timer(self.globalvars)
		
	def load_from_xml_node(self, highscore_node) :

		# initializes score from XML

		self.name = highscore_node.getAttribute("name")

		self.datetime = highscore_node.getAttribute("datetime")
	
		good_answers_str = highscore_node.getAttribute("good_answers")

		if (cmp(good_answers_str, "") != 0) :
			self.good_answers = int(good_answers_str)
			self.count_good = True


		wrong_answers_str = highscore_node.getAttribute("wrong_answers")
		if (cmp(wrong_answers_str, "") != 0) :
			self.wrong_answers = int(wrong_answers_str)
			self.count_wrong = True



		time_str = int(highscore_node.getAttribute("time"))

		if (cmp(time_str, "") != 0) :
			time = int(time_str)

			self.record_time = True

			self.timer.stored_milliseconds = time



	def enable_count_good(self) :
		self.count_good = True

	def enable_count_wrong(self) :
		self.count_wrong = True

	def enable_record_time(self) :
		self.record_time = True

	def good_answer(self) :

		self.good_answers = self.good_answers + 1

	def wrong_answer(self) :

		self.wrong_answers = self.wrong_answers + 1

	def get_name(self) :
		return self.name

	def get_good_answers_value(self) :
		return self.good_answers

	def get_wrong_answers_value(self) :
		return self.wrong_answers

	def get_time_toString(self) :
		return self.timer.toString()

	def get_arcade_mode(self) :
		# returns true if some 'arcade' element is allowed by this score object AND arcade mode is globally allowed
		# returns false if all the 'arcade' elements have been disabled for the activity or arcade mode is globally disabled

		return ((self.count_good or self.count_wrong or self.record_time) and self.globalvars.arcade_mode)


	def good_answers_toString(self) :
		return str(self.good_answers)



	def wrong_answers_toString(self) :
		return str(self.wrong_answers)


	def add(self, other_score) :
		# adds another score to the Score object
		# (useful to compute total scores)

		# this might be not needed anymore => dead code
		# TODO : remove 

		self.good_answers = other_score.good_answers + self.good_answers
		self.wrong_answers = other_score.wrong_answers + self.wrong_answers
		self.timer.add(other_score.timer)

		self.count_good = self.count_good or other_score.count_good 
		self.count_wrong = self.count_wrong or other_score.count_wrong
		self.record_time = self.record_time or other_score.record_time


		


def score_cmp(score1, score2) :

	points1 = score1.get_good_answers_value() - score1.get_wrong_answers_value()
	points2 = score2.get_good_answers_value() - score2.get_wrong_answers_value()

	if (points1 != points2) :
		return cmp(points1, points2)

	time1 = score1.timer.getValue()
	time2 = score2.timer.getValue()

	return cmp(time1, time2)

class Timer() :
	# class used to measure time in arcade mode
	def __init__(self, globalvars) :

		self.globalvars = globalvars

		self.stored_milliseconds = 0

		self.init_value =  pygame.time.get_ticks()

		self.running = False


	def run(self) :

		if (self.running == True) :
			warn("Request to run the timer... but it was already running !!!")

		else :
			self.running = True

			self.init_value = pygame.time.get_ticks()

			info("Running timer / init value = " + str(self.init_value))


	def stop(self) :

		if (self.running == False) :
			warn("Request to stop the timer... but it was already stopped !!!")

		else :

			self.running = False

			self.stored_milliseconds = self.stored_milliseconds + pygame.time.get_ticks() - self.init_value

			info("Stopping timer / stored milliseconds = " + str(self.stored_milliseconds))


	def getValue(self) :
		milliseconds = self.stored_milliseconds

		if (self.running == True) :
			milliseconds = milliseconds + (pygame.time.get_ticks() - self.init_value)

		return milliseconds


	def toString(self) :

		milliseconds = self.getValue()

		# converts a value in milliseconds into a string to display on the timer_text

		minutes = milliseconds // 60000

		milliseconds = milliseconds % 60000

		seconds = milliseconds // 1000


		if (minutes > 0) :
			text_minutes = string.rjust(str(minutes),3, " ")+":"
		else :
			text_minutes = "    "

		if (minutes > 0) :
			text = text_minutes + string.rjust(str(seconds),2, "0")
		else :
			text = text_minutes + string.rjust(str(seconds),2, " ")

		return text

	def add(self, other_timer) :

		self.stored_milliseconds = self.stored_milliseconds + other_timer.stored_milliseconds

