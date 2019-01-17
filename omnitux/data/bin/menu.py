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

import sys, os, codecs
		
import common, constants

# redirect the output to the log file
try :
	if (not os.path.isdir(constants.home_dir)) :
		os.mkdir(constants.home_dir)

	if (not os.path.isdir(constants.folder_log)) :
		os.mkdir(constants.folder_log)

	sys.stdout = codecs.open(constants.log_file, encoding='utf-8', mode='a+')
	sys.stderr = codecs.open(constants.log_file, encoding='utf-8', mode='a+')

except :
	print "Impossible to write inside the log file (" + constants.log_file + "). Game will nevertheless try to run."


try :
	# try to import pygame
	import pygame
	from pygame.locals import *
except :
	from Tkinter import *
	from SimpleDialog import SimpleDialog

	root = Tk()

	common.error("pygame is not available. Please install pygame on your system.")
	
	SimpleDialog(root,
             i18n.get_text(common.get_user_lang(), 102) + "\n" + i18n.get_text(common.get_user_lang(), 104),
             ["OK"],
             0,
             title="Omnitux").go()
	
	exit()


try :
	# try to import pygtk
	import pygtk

except :
	from Tkinter import *
	from SimpleDialog import SimpleDialog

	root = Tk()

	common.error("pygtk is not available. Please install pygtk on your system.")
	
	SimpleDialog(root,
             i18n.get_text(common.get_user_lang(), 103) + "\n" + i18n.get_text(common.get_user_lang(), 104),
             ["OK"],
             0,
             title="Omnitux").go()

	exit()


common.info("Starting Omnitux")

globalvars = common.init()

common.info("Omnitux release = "+globalvars.release)

common.info("Version = "+constants.version)

common.info("Showing screen")
pygame.display.flip()


# activities and other stuff are imported here and not at the beginning

# the idea is to show a black screen as soon as possible so that
# the user won't click again on the omnitux icons_amount
# (especially for slow systems)


import random, copy, traceback, math

import ui, xml_funcs, i18n

import igloo, associate, puzzle, memory_cards, differences, transform, highscore, learning, options


# TODO : make a better support of both fonts !

#globalvars.fonts = ui.Fonts(os.path.join(constants.folder_fonts, constants.fonts_name))
globalvars.fonts = ui.Fonts(os.path.join(constants.folder_fonts, "wqy-microhei.ttc"))


class Page_menu(ui.Page) :

	# list all the activities to select one

	def __init__(self, globalvars, tag_defs) :
		
		self.text_height = 10

		background = constants.main_menu_back
		
		self.games_list = Games_List(globalvars)

		self.igloo_page = None
		self.highscore_page = None

		self.page_type = None

		self.tag_defs = tag_defs

		ui.Page.__init__(self, globalvars, background, "FILL")

	
	def update(self) :
		
		ui.Page.update(self)
		
		# adding the omnitux logo
		self.omnitux_logo_image = ui.Image(self, (35,35), (30, 30), constants.omnitux_logo)

		self.append_back(self.omnitux_logo_image)

		self.draw_back()


		# TODO clean next line someday (split in two pages ?)
		self.second_background_image = ui.Image(self, (0,0), (100,100), constants.main_menu_second_back, 255, 100, "FILL")


	def display_main_menu(self) :

		self.remove_all()

		self.quit_icon = ui.Image(self, constants.stop_icon_pos, constants.stop_icon_size, constants.stop_icon)
		self.append(self.quit_icon)
		
		self.options_icon = ui.Image(self, constants.options_icon_pos, constants.options_icon_size, constants.options_icon_file)
		self.options_icon.set_associated_text(i18n.get_text(self.language, 105))
		self.append(self.options_icon)
		self.listen_to_mouse_over(self.options_icon)

		self.tag_icons = []

		for tag_def in self.tag_defs :

			tag = tag_def.tag

			games_with_this_tag = self.games_list.get_games_by_tag_and_language(tag, self.language) 

			if (len(games_with_this_tag) > 0) :

				image_filename = tag_def.image_filename
				text = tag_def.get_text(self.language)

				tag_icon = ui.Image(self, (0,0), (11,11), image_filename)
				tag_icon.set_associated_text(text)
				self.append(tag_icon)
				self.listen_to_mouse_over(tag_icon)
				tag_icon.set_associated_object(tag_def)

				self.tag_icons.append(tag_icon)

		self.igloo_image = ui.Image_Absolute(self, self.igloo_page.surface_to_zoom_rect.topleft, self.igloo_page.surface_to_zoom_rect.size , self.igloo_page.igloo_reduced_surface)

		self.igloo_image.set_associated_text(i18n.get_text(self.language, 1020))
		self.append(self.igloo_image)
		self.listen_to_mouse_over(self.igloo_image)


		self.init_country_flags()

		(igloo_width, igloo_height) = constants.igloo_size

		self.language_image = ui.Image(self, (((self.igloo_page.flag_mast_pos_x * igloo_width)/100.0), constants.main_flag_pos_y + ((self.igloo_page.flag_mast_pos_y * igloo_height)/100.0)), constants.main_flag_size, i18n.countries_prefix + self.countries[self.country_index] + i18n.countries_suffix, 255, 100, "BOTTOMLEFT")
		self.language_image.outline(constants.flag_outline_color, constants.flag_outline_width)
		self.language_image.set_associated_text(i18n.get_text(self.language, self.language))
		self.append(self.language_image)
		self.listen_to_mouse_over(self.language_image)


		# will play the sound of the 'next' language when the user clicks the language textbox
		next_lang_index = constants.supported_languages.index(self.language) + 1
		if (next_lang_index >= len(constants.supported_languages)) :
			next_lang_index = 0

		self.language_image.associated_sounds = i18n.language_sound[constants.supported_languages[next_lang_index]]


		circle_icons = Circle_icons(self, self.omnitux_logo_image.rect.center, self.omnitux_logo_image.rect.size, 2.1, len(self.tag_icons))


		for tag_icon in self.tag_icons :

			tag_icon.set_center_abs(circle_icons.get_center())



		self.append(ui.Text(self, i18n.get_text(self.language, 1102), (0,94), (100, 3), self.fonts, constants.text_color, 1))
		self.append(ui.Text(self, i18n.get_text(self.language, 1103), (0,97), (100, 3), self.fonts, constants.text_color, 1))
		

		self.page_type = "MAIN"

		return [self.screen.get_rect()]		


	def display_games_by_type(self) :

		self.fade_out()

		self.remove_all()
		

		self.append(self.second_background_image)

		self.append(ui.Box(self, self.legend_text_pos, self.legend_text_size, constants.button_box_color))


		if (len(self.games_to_display) > 0) :

			circle_icons = Circle_icons(self, self.omnitux_logo_image.rect.center, self.omnitux_logo_image.rect.size, 2.1, len(self.games_to_display))

			index = 0

			for games in self.games_to_display :

				#x_pos = index % amount_x
				#y_pos = index // amount_x
		
				#offset_x = step_x * x_pos
				#offset_y = step_y * y_pos

				text = games.get_title(self.language)

				icon = ui.Image(self, (0,0), (11,11), games.get_thumb())

				icon.set_associated_text(text)

				self.listen_to_mouse_over(icon)
				
				icon.set_associated_object(games)

				icon.set_center_abs(circle_icons.get_center())

				self.append(icon)
				
				index = index + 1

		
		self.go_back_icon = ui.Image(self, constants.go_left_icon_pos, constants.go_left_icon_size, constants.go_left_icon)
		self.append(self.go_back_icon)
		
		self.draw()
		
		self.page_type = "GAME_SELECTION"
		
		return [self.screen.get_rect()]

	def display_quit(self) :
		self.remove_all()
		
		self.append(ui.Box(self, (10, 39), (80,22), constants.button_box_color))
	
		self.append(ui.Text(self, i18n.get_text(self.language, 1105), (10, 40), (80, 10), self.fonts, constants.text_color, 1))
		
		self.quit_yes = ui.TextBox(self, i18n.get_text(self.language, 100), (10, 50), (40, 10), self.fonts, constants.text_color, 11, constants.stop_icon)
		self.quit_no = ui.TextBox(self, i18n.get_text(self.language, 101), (50, 50), (40, 10), self.fonts, constants.text_color, 11, constants.go_next_icon)
		
		self.append(self.quit_yes)
		self.append(self.quit_no)
		
		self.page_type = "DIALOG_BOX_QUIT"
		
					
		self.draw()
		return [self.screen.get_rect()]



	def run_igloo(self, new_tux) :
		self.fade_out()

		if (new_tux == True) :
			self.igloo_page.new_tux()
	
		igloo.Run_Igloo(self.igloo_page)
		
		self.igloo_image.surface = self.igloo_page.igloo_reduced_surface

		self.igloo_image.draw()


	def run_highscore(self, level, total_score = None) :
		self.fade_out()

		if (self.highscore_page == None) :
			self.highscore_page = highscore.create(self.globalvars)

	
		highscore.Run_Highscore(self.highscore_page, level, total_score)
		



class Circle_icons() :

	def __init__(self, page, (center_x, center_y), (width, height), ratio, icons_amount) :
		
		self.page = page
		
		(self.center_x, self.center_y) = (center_x, center_y)

		(self.width, self.height) = (width/2, height/2)

		self.ratio = ratio

		self.icons_amount = icons_amount

		# the idea is to order the icons by approximative 'difficulty level' 
		# on a circle similar to the speed-o-meter of a car

		self.current_angle = ((7.0*math.pi)/8.0)

		if (self.icons_amount > 1) :
			self.angle_step = (((5.0*math.pi)/4.0)/(self.icons_amount-1))
		else :
			# useless, just to avoid division by zero
			self.angle_step = 0


	def get_center(self) :

		pos_x = self.center_x + ((self.width * math.cos(self.current_angle)) * self.ratio)
		pos_y = self.center_y + ((self.height * math.sin(self.current_angle)) * self.ratio)

		self.current_angle = self.current_angle + self.angle_step

		return (pos_x, pos_y)


class Page_level(ui.Page) :

	# list all the activities to select one

	def __init__(self, globalvars, second_background_image) :
		
		self.text_height = 10

		# background = constants.omnitux_logo
	
		self.page_type = "SELECT_LEVEL"

		self.second_background_image = second_background_image

		ui.Page.__init__(self, globalvars, None, "CENTERED")


	def select_level(self, levels) :

		self.append(self.second_background_image)

		self.go_back_icon = ui.Image(self, constants.go_left_icon_pos, constants.go_left_icon_size, constants.go_left_icon)
		self.append(self.go_back_icon)

		self.append(ui.Rounded_Box(self, (10, 10), (80, 83), constants.button_box_color))

		self.append(ui.Text(self, i18n.get_text(self.language, 1106), (10, 25), (80, 10), self.fonts, constants.text_color, 1))

		step_x = 80.0 / len(levels)
		
		offset_x = 50.0 - (step_x * (len(levels) / 2.0))

		index = 0

		for level in levels :
			level_image = ui.Image(self, (offset_x, 51) , (step_x, 23), level.get_difficulty_level_image())

			level_image.set_associated_object(level)

			offset_x = offset_x + step_x

			self.append(level_image)

			index = index + 1

		self.page_type = "SELECT_LEVEL"

		self.draw()
		return [self.screen.get_rect()]	
	

class Games_List() :
	# object which groups a set of games titles
	
	def __init__(self, globalvars) :
		self.games_list = []

		self.globalvars = globalvars
	
	def append_from_folder(self, folder) :
		# recursively appends all the XML game files
		# which are found inside a folder
		xml_files = common.get_files(folder, ["xml"])		
		
		for xml_file in xml_files :

			try :
				games = common.Game_set(self.globalvars, xml_file)
			
				self.games_list.append(games)

			except Exception, e :
				common.error("Could not cope with " + xml_file)
				common.error("Problem in XML file reading ", e, traceback.format_exc())

	
	def get_games_by_tag_and_language(self, selected_tag, lang) :
		
		selected_games = []
		
		for game_set in self.games_list :

			tags = game_set.get_tags()

			for tag in tags :

				if (cmp(tag, selected_tag) == 0) :
					
					if (game_set.get_title(lang) != None) :
						# we add the games in the selected language
						selected_games.append(game_set)

		
		selected_games.sort(lambda x, y: cmp(x.get_menu_index(lang) + x.get_title(lang), y.get_menu_index(lang) + y.get_title(lang)))
		
		return selected_games


class Run_Menu(common.Run_Screen) :

	def __init__(self, globalvars) :

		common.Run_Screen.__init__(self, globalvars)	

		tag_defs = common.load_tag_defs()

		self.current_page = Page_menu(globalvars, tag_defs)

		self.current_page.draw_back()
		pygame.display.flip()

		common.start_music(constants.default_music_files, globalvars)

		common.info("Looking for xml activities")
		for data_folder in constants.data_folders :
			self.current_page.games_list.append_from_folder(data_folder)

		common.info("Initialize igloo")
		self.current_page.igloo_page = igloo.create(self.globalvars)

		common.info("Display main menu")
		self.current_page.display_main_menu()
	
		self.current_page.draw()
		pygame.display.flip()

		main_page = self.current_page
	
		level = None

		while self.running :

			try :

				common.Run_Screen.run_pre(self)

			except common.EndActivityException, e :

				# although we should normally end after an EndActivityException,
				# here we'll ask for user confirmation
				self.running = True

				if (cmp(self.current_page.page_type, "MAIN") == 0) :

					self.dirty_rects = self.current_page.display_quit()

				elif (cmp(self.current_page.page_type, "SELECT_LEVEL") == 0) :
		
					self.mouse_clicked = False

					self.current_page = main_page
					self.current_page.draw()

					self.dirty_rects = [self.screen.get_rect()]

		
				else :
		
					self.dirty_rects = self.current_page.display_main_menu()

					self.current_page.draw()


			if (self.mouse_clicked == True) :
				clicked = self.current_page.was_something_clicked(self.mouse_pos, self.mousebutton)
		
				if (clicked != None) :
					(component_clicked, foo, some_dirty_rects) = clicked

					self.dirty_rects = self.dirty_rects + some_dirty_rects

					if (component_clicked != None) :
						# we try to play an associated sound (if any)
						component_clicked.play_random_associated_sound()


					if (cmp(self.current_page.page_type, "DIALOG_BOX_QUIT") == 0) :
						if (component_clicked == self.current_page.quit_yes) :
							self.running = False
					
						elif (component_clicked == self.current_page.quit_no):

							self.dirty_rects = self.current_page.display_main_menu()

							self.current_page.draw()

							self.mouse_clicked = False


					elif (cmp(self.current_page.page_type, "MAIN") == 0) :
			
						if (component_clicked == self.current_page.igloo_image) :
		
							self.current_page.run_igloo(False)
					
							self.mouse_clicked = False

							self.current_page = main_page

							self.current_page.draw()

							self.dirty_rects = [self.screen.get_rect()]

						elif (component_clicked == self.current_page.language_image) :
					
							# changing main language
					
							self.current_page.remove_all()
					
							index_lang = constants.supported_languages.index(self.current_page.language)
					
							index_lang = index_lang + 1
					
							if (index_lang >= len(constants.supported_languages)) :
								index_lang = 0
						
							self.current_page.language = constants.supported_languages[index_lang]

							self.globalvars.main_language = constants.supported_languages[index_lang]
					
							self.dirty_rects =  self.current_page.display_main_menu()
					
							self.current_page.draw()

			
							self.mouse_clicked = False			
				
						elif (component_clicked == self.current_page.quit_icon) :
					
							self.dirty_rects = self.current_page.display_quit()
				
							self.mouse_clicked = False
				
						elif (component_clicked in self.current_page.tag_icons ) :

							# TODO : allow multiple activities inside a game_set !
				
							tag_icon = component_clicked
							tag_def = tag_icon.associated_object

							self.current_page.games_to_display = self.current_page.games_list.get_games_by_tag_and_language(tag_def.tag, self.current_page.language)
					
							self.dirty_rects = self.current_page.display_games_by_type()
					
							self.mouse_clicked = False

						elif (component_clicked == self.current_page.options_icon) :
							
							self.current_page.fade_out()

							options.Run_options(globalvars) 

							self.current_page.draw()
							
							pygame.display.flip()

							self.mouse_clicked = False
			
					elif (cmp(self.current_page.page_type, "GAME_SELECTION") == 0) :


						if (component_clicked == self.current_page.go_back_icon) :
							self.current_page.fade_out()

							self.dirty_rects = self.current_page.display_main_menu()	
							self.current_page.draw()

							self.mouse_clicked = False
				
						else :
							game_set = component_clicked.associated_object
				
							if (game_set != None) :

								# TODO allow more levels !!!!
								levels = game_set.levels

								if (len(levels) > 1) :

									level_page = Page_level(globalvars, self.current_page.second_background_image)

									self.current_page = level_page


									self.dirty_rects = self.current_page.select_level(levels)

									self.mouse_clicked = False

								else :
									# in case we have a single level activity
									level = levels[0]






					elif (cmp(self.current_page.page_type, "SELECT_LEVEL") == 0) :

						if (component_clicked == self.current_page.go_back_icon) :

							# TODO : a implementer !!!

							self.mouse_clicked = False

							self.current_page = main_page
							self.current_page.draw()

							self.dirty_rects = [self.screen.get_rect()]
	
						else :
							associated_object = component_clicked.associated_object
				
							if (associated_object != None) :

								self.current_page.fade_out()

								# TODO allow more levels !!!!
								level = associated_object

			else :
				# mouse is not clicked
				# but it may be going over elements

				(mouse_over_new, mouse_over_old) = self.current_page.components_mouse_over(pygame.mouse.get_pos())


				if (mouse_over_old != None) :
					self.dirty_rects = self.dirty_rects + self.current_page.remove_legend_text()


				if (mouse_over_new != None) :
					self.dirty_rects = self.dirty_rects + self.current_page.add_legend_text(mouse_over_new)


			if (level != None) :

				# then we'll go back to main page when game or highscore will end
				self.current_page = main_page	
				
				if (self.mousebutton == 3) :
				
					# right click means start highscore screen

					self.current_page.run_highscore(level)
			
					self.mouse_clicked = False

				else :


					self.current_page.fade_out()


					# the level is copied in order to change its variables
					copy_level = copy.copy(level)

	

					# shuffle the games
					copy_level.games = common.randomize_list(copy.copy(copy_level.games))

					amount_games_played = 0

					try :

						total_score = common.Score(globalvars)

						for game in copy_level.games :

							if (amount_games_played < copy_level.game_rounds_amount) :

								if (cmp(game.game_type, "associate") == 0) :
									# association
									run_activity = associate.Run_Associate(game, globalvars, total_score) 
					
								if (cmp(game.game_type, "puzzle") == 0) :
									# puzzle
									run_activity = puzzle.Run_Puzzle_Screen(game, globalvars, total_score)

								if (cmp(game.game_type, "memory_cards") == 0) :
									# memory cards
									run_activity = memory_cards.Run_Memory_Cards_Screen(game, globalvars, total_score)

								if (cmp(game.game_type, "differences") == 0) :
									# differences
									run_activity = differences.Run_Differences_Screen(game, globalvars, total_score)

								if (cmp(game.game_type, "transform") == 0) :
									# image transformation
									run_activity = transform.Run_Transform_Screen(game, globalvars)

								if (cmp(game.game_type, "learning") == 0) :
									# learning cards
									run_activity = learning.Run_Learning_Screen(game, globalvars)

								amount_games_played = amount_games_played + 1


							else :
								# if all the games were played, there's nothing more to play !
						
								common.info("Not enough games left to play. Level completed.")
		
						if (pygame.mixer.music.get_busy() == False) :
							common.start_music(constants.default_music_files, globalvars)


						# we go to the highscore screen, if activated and if some score was indeed recorded
						if ((total_score.get_arcade_mode() == True) and (self.globalvars.highscore == True)) :
							self.current_page.run_highscore(copy_level, total_score)
		
						# After a completed game_set, we get a Tux as a reward
						# (only in case the display_igloo global var is True
						if (self.globalvars.display_igloo == True) :
							self.current_page.run_igloo(True)
				
			
						self.dirty_rects = []

					except common.EndActivityException, e :
						common.info("Activity stopped by the user")
			
					except common.BadXMLException, e:
						common.error("Had to stop the activity because of an error in XML setup")

					except Exception, e :
						common.error("Exception fired", e, traceback.format_exc())				
		
	
					try :
						if (pygame.mixer.music.get_busy() == False) :
							common.start_music(constants.default_music_files, globalvars)
					except Exception, e :
						common.error("Problem with playing music", e, traceback.format_exc())	

				self.current_page.draw()
		
				self.dirty_rects = [self.screen.get_rect()]

				self.mouse_clicked = False

				level = None


			# flag animation
			if (self.current_page.page_type == "MAIN") :
				self.dirty_rects = self.dirty_rects + self.current_page.next_country()
			else :
				self.current_page.country_ticks = 0


			common.Run_Screen.run_post(self)	




Run_Menu(globalvars) 



common.info("Leaving Omnitux")

pygame.mixer.quit()

common.info("After mixer quit")

pygame.display.quit()

common.info("After display quit")
