# -*- coding: utf-8 -*-

# Omnitux - educational activities based upon multimedia elements
# Copyright (C) 2010 Olav_2 (olav.olav@yahoo.fr)
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

import pygame, os

import common, constants, ui, i18n


# on option screen itself :
constant_topimage_pos = (0, 0)
constant_topimage_size = (100, 20)
constant_topimage_file = "default/options/Cockpit_top.jpg"

constant_bottomimage_pos = (0, 65)
constant_bottomimage_size = (100, 35)
constant_bottomimage_file = "default/options/Cockpit_bottom.jpg"

constant_hud_color = (136, 205, 146)
constant_negative_hud_color = (0, 0, 0)

constant_restart_text_pos = (0, 21)
constant_restart_text_size = (100, 3)

constant_resolution_text_pos = (0, 30)
constant_resolution_text_size = (24, 3)

constant_resolution_minus_pos = (25, 30)
constant_resolution_minus_size = (1.5, 3)

constant_resolution_value_pos = (27, 30)
constant_resolution_value_size = (10, 3)

constant_resolution_plus_pos = (37.5, 30)
constant_resolution_plus_size = (1.5, 3)


constant_music_text_pos = (0, 34)
constant_music_text_size = (24, 3)

constant_music_minus_pos = (25, 34)
constant_music_minus_size = (1.5, 3)

constant_music_value_pos = (27, 34)
constant_music_value_size = (10, 3)

constant_music_plus_pos = (37.5, 34)
constant_music_plus_size = (1.5, 3)


constant_igloo_text_pos = (0, 38)
constant_igloo_text_size = (24, 3)

constant_display_igloo_pos = (27, 38)
constant_display_igloo_size = (5, 3)


constant_arcade_mode_text_pos = (0, 42)
constant_arcade_mode_text_size = (24, 3)

constant_arcade_mode_pos = (27, 42)
constant_arcade_mode_size = (5, 3)


class Page_options(ui.Page) :

	def __init__(self, globalvars) :

		background = constants.main_menu_back

		self.restart_text = None

		ui.Page.__init__(self, globalvars, background, "FILL")

	def update(self) :

		ui.Page.update(self)

		# finish the background

		self.omnitux_logo_image = ui.Image(self, (35,25), (30, 30), constants.omnitux_logo)

		self.append_back(self.omnitux_logo_image)

		self.append_back(ui.Image(self, constant_topimage_pos, constant_topimage_size, constant_topimage_file, 255, 100, "FILL"))

		self.append_back(ui.Image(self, constant_bottomimage_pos, constant_bottomimage_size, constant_bottomimage_file, 255, 100, "FILL"))

		self.draw_back()




		self.go_back_icon = ui.Image(self, constants.go_left_icon_pos, constants.go_left_icon_size, constants.go_left_icon)
		self.append(self.go_back_icon)


		# screen resolution
		self.append(ui.Text(self, i18n.get_text(self.language, 200), constant_resolution_text_pos, constant_resolution_text_size, self.fonts, constant_hud_color, 2))

		self.resolution_minus = ui.TextBox(self, "-", constant_resolution_minus_pos, constant_resolution_minus_size, self.fonts, constant_negative_hud_color, 1, None, 255, constant_hud_color)

		self.append(self.resolution_minus)


		(self.globalvars.screen_width, self.globalvars.screen_height) = (self.screen.get_size())
	
		self.resolution_value = ui.TextBox(self, str(self.globalvars.screen_width)+"x"+str(self.globalvars.screen_height), constant_resolution_value_pos, constant_resolution_value_size, self.fonts, constant_negative_hud_color, 1, None, 255, constant_hud_color)

		self.append(self.resolution_value)

		self.resolution_plus = ui.TextBox(self, "+", constant_resolution_plus_pos, constant_resolution_plus_size, self.fonts, constant_negative_hud_color, 1, None, 255, constant_hud_color)

		self.append(self.resolution_plus)

		self.available_resolutions = pygame.display.list_modes()

		self.current_resolution_index = self.available_resolutions.index((self.globalvars.screen_width, self.globalvars.screen_height))

		# music volume
		self.append(ui.Text(self, i18n.get_text(self.language, 201), constant_music_text_pos, constant_music_text_size, self.fonts, constant_hud_color, 2))

		self.music_minus = ui.TextBox(self, "-", constant_music_minus_pos, constant_music_minus_size, self.fonts, constant_negative_hud_color, 1, None, 255, constant_hud_color)

		self.append(self.music_minus)

		self.music_value = ui.TextBox(self, str(int(self.globalvars.music_volume * 100))+"%", constant_music_value_pos, constant_music_value_size, self.fonts, constant_negative_hud_color, 1, None, 255, constant_hud_color)

		self.append(self.music_value)

		self.music_plus = ui.TextBox(self, "+", constant_music_plus_pos, constant_music_plus_size, self.fonts, constant_negative_hud_color, 1, None, 255, constant_hud_color)

		self.append(self.music_plus)

		# igloo yes/no
		self.append(ui.Text(self, i18n.get_text(self.language, 1020), constant_igloo_text_pos, constant_igloo_text_size, self.fonts, constant_hud_color, 2))

		self.display_igloo = ui.TextBox(self, i18n.bool_to_text(self.language, self.globalvars.display_igloo), constant_display_igloo_pos, constant_display_igloo_size, self.fonts, constant_negative_hud_color, 1, None, 255, constant_hud_color)

		self.append(self.display_igloo)


		# "no stress" vs "arcade" => commented until the feature will be developped
		#### self.append(ui.Text(self, i18n.get_text(self.language, 220), constant_arcade_mode_text_pos, constant_arcade_mode_text_size, self.fonts, constant_hud_color, 2))

		self.arcade_mode = ui.TextBox(self, i18n.bool_to_text(self.language, self.globalvars.arcade_mode), constant_arcade_mode_pos, constant_arcade_mode_size, self.fonts, constant_negative_hud_color, 1, None, 255, constant_hud_color)

		#### self.append(self.arcade_mode)


		self.draw()


	def display_restart(self) :

		if (self.restart_text == None) :

			self.restart_text = ui.Text(self, i18n.get_text(self.language, 210), constant_restart_text_pos, constant_restart_text_size, self.fonts, constant_hud_color, 1)

			self.append(self.restart_text)

			return self.restart_text.draw()

		else :

			return []


class Run_options(common.Run_Screen) :
	
	def __init__(self, globalvars) :

		common.info("Running options screen")

		self.globalvars = globalvars

		common.Run_Screen.__init__(self, self.globalvars)

		self.current_page = Page_options(self.globalvars)

		self.current_page.draw()
		pygame.display.flip()
		
		while self.running :

			try :

				common.Run_Screen.run_pre(self)

			except common.EndActivityException, e :
				self.running = False



			if (self.mouse_clicked == True) :
				clicked = self.current_page.was_something_clicked(self.mouse_pos, self.mousebutton)
	
				if (clicked != None) :

					self.mouse_clicked = False

					(component_clicked, foo, some_dirty_rects) = clicked

					if (component_clicked == self.current_page.go_back_icon) :

						self.running = False


					elif (component_clicked == self.current_page.resolution_minus) :
						self.current_page.current_resolution_index = self.current_page.current_resolution_index + 1

						if (self.current_page.current_resolution_index >= len(self.current_page.available_resolutions)) :
							self.current_page.current_resolution_index = len(self.current_page.available_resolutions) - 1

						else :

							(self.globalvars.screen_width, self.globalvars.screen_height) = self.current_page.available_resolutions[self.current_page.current_resolution_index]

							self.current_page.resolution_value.set_text(str(self.globalvars.screen_width)+"x"+str(self.globalvars.screen_height))

							self.dirty_rects = self.current_page.resolution_value.draw()  + self.current_page.display_restart()


					elif (component_clicked == self.current_page.resolution_plus) :
						self.current_page.current_resolution_index = self.current_page.current_resolution_index - 1

						if (self.current_page.current_resolution_index < 0) :
							self.current_page.current_resolution_index = 0

						else :

							(self.globalvars.screen_width, self.globalvars.screen_height) = self.current_page.available_resolutions[self.current_page.current_resolution_index]

							self.current_page.resolution_value.set_text(str(self.globalvars.screen_width)+"x"+str(self.globalvars.screen_height))

							self.dirty_rects = self.current_page.resolution_value.draw() + self.current_page.display_restart()



					elif ((component_clicked == self.current_page.music_minus) or (component_clicked == self.current_page.music_plus)) :

						
						if (component_clicked == self.current_page.music_minus) :
							self.current_page.globalvars.music_volume = self.current_page.globalvars.music_volume - 0.25
							
							if (self.current_page.globalvars.music_volume < 0) :
								self.current_page.globalvars.music_volume = 0.0

						elif (component_clicked == self.current_page.music_plus) :
							self.current_page.globalvars.music_volume = self.current_page.globalvars.music_volume + 0.25

							if (self.current_page.globalvars.music_volume > 1) :
								self.current_page.globalvars.music_volume = 1.0

						self.current_page.music_value.set_text(str(int(self.current_page.globalvars.music_volume * 100)) + "%")

						self.set_music_volume(self.current_page.globalvars.music_volume)

						self.dirty_rects = self.current_page.music_value.draw()


					elif (component_clicked == self.current_page.display_igloo) :
						
						self.globalvars.display_igloo = not(self.globalvars.display_igloo)

						self.current_page.display_igloo.set_text(i18n.bool_to_text(self.current_page.language, self.globalvars.display_igloo))

						self.dirty_rects = self.current_page.display_igloo.draw()


					elif (component_clicked == self.current_page.arcade_mode) :
						
						self.globalvars.arcade_mode = not(self.globalvars.arcade_mode)

						self.current_page.arcade_mode.set_text(i18n.bool_to_text(self.current_page.language, self.globalvars.arcade_mode))

						self.dirty_rects = self.current_page.arcade_mode.draw()

					# we may call this a bit too often, but it's easier for code maintenance :-)
					self.globalvars.save_user_options()


			common.Run_Screen.run_post(self)	


class Options_screen :

	def __init__(self) :

		(self.language, foo) = common.get_user_lang()


		self.globalvars = common.GlobalVars()



		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)

		self.window.set_title(i18n.get_text(self.language, 105))
		self.window.set_border_width(10)

		self.window.connect("delete_event", self.delete_event)

		self.notebook = gtk.Notebook()
		self.notebook.set_tab_pos(gtk.POS_LEFT)

		general_panel = General_panel(self)
		language_panel = Language_panel(self)

		self.window.add(self.notebook)

		self.window.show_all()


	def main(self) :
		gtk.main()

		return 0



	def delete_event(self, widget, event, data=None):

		self.globalvars.save_user_options()

		gtk.main_quit()

		return False




class General_panel :

	def __init__(self, options_screen) :

		# TODO : more on this
		self.language = options_screen.language
		self.globalvars = options_screen.globalvars


		self.vbox = gtk.VBox(False, constants.vpad)


		# Screen resolution selection

		### display options ###

		display_frame = gtk.Frame(i18n.get_text(self.language, 202)) # Display


		hbox = gtk.HBox(False, 10)

		label = gtk.Label(i18n.get_text(self.language, 200)) # Screen resolution
		
		hbox.pack_start(label, False)

		self.resolution_combo = gtk.combo_box_new_text()
	
		self.resolution_combo.connect("changed", self.change_resolution)

		self.resolution_combo.set_wrap_width(4)
		

		self.available_resolutions = pygame.display.list_modes()

		i = 0

		for resolution in self.available_resolutions :

			(width, height) = resolution

			self.resolution_combo.append_text(str(width)+"x"+str(height))
		
			if ((self.globalvars.screen_width == width) and (self.globalvars.screen_height == height)) :

				self.resolution_combo.set_active(i)

			i = i + 1
			

		hbox.pack_start(self.resolution_combo, False)

		display_frame.add(hbox)

		self.vbox.pack_start(display_frame, False)


		### sound options ###

		sound_frame = gtk.Frame(i18n.get_text(self.language, 203)) # Sound

		# Music volume

		vbox = gtk.VBox(False, constants.vpad)

		hbox = gtk.HBox(False, constants.hpad)

		label = gtk.Label(i18n.get_text(self.language, 201))
		
		hbox.pack_start(label, False, True, constants.hpad)

		self.volume_buttons = []

		self.volume_buttons.append(gtk.RadioButton(None, "0"))
		self.volume_buttons[0].connect("toggled", self.toggle_music_volume, 0)

		hbox.pack_start(self.volume_buttons[0], False, True, constants.hpad)

		for volume in range(1, 5) :
			self.volume_buttons.append(gtk.RadioButton(self.volume_buttons[0], str(volume * 25)))

			self.volume_buttons[volume].connect("toggled", self.toggle_music_volume, volume/4.0)

			if (self.globalvars.music_volume == volume / 4.0) :
				self.volume_buttons[volume].set_active(True)

			hbox.pack_start(self.volume_buttons[volume], False, True, constants.hpad)
		

		vbox.pack_start(hbox, False)


		congrats_frame = gtk.Frame(i18n.get_text(self.language, 208))

		
		vbox2 = gtk.VBox(False, constants.vpad)


		self.congrats_sounds_checkbutton = gtk.CheckButton(i18n.get_text(self.language, 204)) # Congratulations sounds
		self.congrats_sounds_checkbutton.set_active(self.globalvars.congrats_sounds_active)
		self.congrats_sounds_checkbutton.connect("toggled", self.toggle)

		vbox2.pack_start(self.congrats_sounds_checkbutton, False)
		

		self.congrats_voices_checkbutton = gtk.CheckButton(i18n.get_text(self.language, 205)) # Congratulations voices
		self.congrats_voices_checkbutton.set_active(self.globalvars.congrats_voices_active)
		self.congrats_voices_checkbutton.connect("toggled", self.toggle)

		vbox2.pack_start(self.congrats_voices_checkbutton, False)
		

		congrats_frame.add(vbox2)

		vbox.pack_start(congrats_frame, False)


		sound_frame.add(vbox)

		self.vbox.pack_start(sound_frame, False)

		
		### misc options ###


		misc_frame = gtk.Frame(i18n.get_text(self.language, 206)) # misc

		# igloo yes / no

		misc_vbox = gtk.VBox()

		self.igloo_checkbutton = gtk.CheckButton(i18n.get_text(self.language, 1020))
		self.igloo_checkbutton.set_active(self.globalvars.display_igloo)
		self.igloo_checkbutton.connect("toggled", self.toggle)

		
		misc_vbox.pack_start(self.igloo_checkbutton, False)

		
		# arcade mode yes / no
		self.arcade_checkbutton = gtk.CheckButton(i18n.get_text(self.language, 220))
		self.arcade_checkbutton.set_active(self.globalvars.arcade_mode)
		self.arcade_checkbutton.connect("toggled", self.toggle)



		misc_vbox.pack_start(self.arcade_checkbutton, False)

		misc_frame.add(misc_vbox)

		self.vbox.pack_start(misc_frame, False)


		hbox = gtk.HBox(False, constants.hpad)

		omnitux_logo_image = gtk.Image()
		omnitux_logo_image.set_from_file(constants.omnitux_logo_small)

		hbox.pack_start(omnitux_logo_image, True, True, constants.hpad)

		label = gtk.Label(i18n.get_text(self.language, 207))
		hbox.pack_start(label, False, True, constants.hpad)

		omnitux_logo_image.show()
		label.show()

		hbox.show()

		options_screen.notebook.append_page(self.vbox, hbox)




	def change_resolution(self, widget) :
		
		(self.globalvars.screen_width, self.globalvars.screen_height) = self.available_resolutions[widget.get_active()]


	def toggle_music_volume(self, foo, music_volume) :

		self.globalvars.music_volume = music_volume



	def toggle(self, widget) :

		if (widget == self.igloo_checkbutton) :	
			self.globalvars.display_igloo = not(self.globalvars.display_igloo)

		elif (widget == self.arcade_checkbutton) :
			self.globalvars.arcade_mode = not(self.globalvars.arcade_mode)

		elif (widget == self.congrats_sounds_checkbutton) :
			self.globalvars.congrats_sounds_active = not(self.globalvars.congrats_sounds_active)

		elif (widget == self.congrats_voices_checkbutton) :
			self.globalvars.congrats_voices_active = not(self.globalvars.congrats_voices_active)


class Language_panel :

	def __init__(self, options_screen) :

		self.globalvars = options_screen.globalvars
		self.language = options_screen.language

		self.vbox = gtk.VBox(False, constants.vpad)


		default_language_frame = gtk.Frame(i18n.get_text(self.language, 250))  # language at startup


		vbox = gtk.VBox()

		self.default_language_system_button = gtk.RadioButton(None, i18n.get_text(self.language, 251)) # system value

		self.default_language_system_button.connect("toggled", self.toggle_default_language_mode, "system")

		vbox.pack_start(self.default_language_system_button, False)

		
		hbox = gtk.HBox(False, constants.hpad)

		self.default_language_user_button = gtk.RadioButton(self.default_language_system_button, i18n.get_text(self.language, 252)) # user value :
		hbox.pack_start(self.default_language_user_button, False)

		self.default_language_user_button.connect("toggled", self.toggle_default_language_mode, "user")

		self.language_combo = gtk.combo_box_new_text()
		
		self.language_combo.connect("changed", self.change_user_default_language)




		i = 0

		for language in self.globalvars.active_languages :
			# TODO use editor language !!
			self.language_combo.append_text(i18n.get_text(language, language))

			if (cmp(language, self.globalvars.main_language) == 0) :
				self.language_combo.set_active(i)

			i = i + 1

		hbox.pack_start(self.language_combo, False)


		vbox.pack_start(hbox, False)

		if (cmp(self.globalvars.main_language_mode, "user") == 0) :
			self.default_language_user_button.set_active(True)

		else :
			self.language_combo.set_sensitive(False)


		default_language_frame.add(vbox)


		self.vbox.pack_start(default_language_frame)


		hbox = gtk.HBox(False, constants.hpad)

		UN_image = gtk.Image()
		UN_image.set_from_file(common.find_file(constants.UN_image_filename, self.globalvars))

		hbox.pack_start(UN_image, True, True, constants.hpad)

		label = gtk.Label(i18n.get_text(self.language, 253))
		hbox.pack_start(label, True, True, constants.hpad)

		UN_image.show()
		label.show()

		hbox.show()

		options_screen.notebook.append_page(self.vbox, hbox)		


	def toggle_default_language_mode(self, foo, main_language_mode) :

		self.globalvars.main_language_mode = main_language_mode

		if (cmp(main_language_mode, "user") == 0) :
			self.language_combo.set_sensitive(True)
			self.change_user_default_language("foo")
		else :
			self.language_combo.set_sensitive(False)


	def change_user_default_language(self, foo) :
		self.globalvars.main_language = self.globalvars.active_languages[self.language_combo.get_active()]


import sys

if (len(sys.argv) > 1) :

	if (cmp(sys.argv[1], "GTK") == 0) :

		import pygtk, gtk

		pygame.init()

		options_screen = Options_screen()
		options_screen.main()



