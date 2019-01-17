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

import pygame, os, random, copy, i18n, string
from pygame.locals import *

import gtk

import common, constants
		
class Sprite() :
	# this is not pygame's sprite class
	# just a very simple custom one instead
	
	def __init__(self, component) :
		self.component = component
		self.background = None
		self.rect_back = None

		# TODO why was the next line removed ??
		self.initial_pos = copy.copy(self.component.rect)
		
	def record_background(self) :
		if (self.component.page.screen.get_clip().colliderect(self.component.rect)) :
			self.background = self.component.page.screen.subsurface(self.component.rect.clip(self.component.page.screen.get_clip())).copy()
			
			self.rect_back = copy.copy(self.component.rect)

	
	def erase(self) :

		if ((self.background != None) and (self.rect_back != None) ):
			
			cut_rect = self.rect_back.clip(self.component.page.screen.get_clip())
			cut_rect.topleft=(0,0)
			
			self.component.page.screen.blit(self.background.subsurface(cut_rect), self.rect_back.clip(self.component.page.screen.get_clip()))

			return [copy.copy(self.rect_back)]
	
		else :
			return []
	
	
		
class Page() :
	# this class is the "root" class for the basic UI items inside a "page" of the game
	
	def __init__(self, globalvars, background_file, background_mode = "FILL") :

		self.globalvars = globalvars

		# initialisation parameters
		self.language = globalvars.main_language     # a string like "fr"
		self.fonts = globalvars.fonts           # the Fonts object which stores used fonts
		self.screen = globalvars.screen         # screen to draw on
		
		self.background_file = background_file
		self.background_mode = background_mode
		self.background = None
		
		# internal entities
		self.items = []              # those are the 'active' items used on screen
		self.items_back = []         # those are the 'static' items drawn directly on the background surface 


		self.items_listen_mouse_over = []	# items which may react to mouse over
		self.last_mouse_over = None	# last object where the mouse was over

		# this should contain an editable component of type 'TextBox'
		# which will receive key events
		# if None, nobody receives any key event
		# TODO : make it work with a Text if needed
		self.activated_component = None
		
		self.activated_text_color = constants.activated_text_color
		self.cursor_color = constants.cursor_color
		
		self.sprites = []
		self.dragged_sprite = None

		self.mouse_component_pointer = Image(self, constants.mouse_initial_pos, constants.mouse_size, constants.mouse_pointer)
		self.mouse_sprite_pointer = Sprite(self.mouse_component_pointer)

		self.mouse_component_drag = Image(self, constants.mouse_initial_pos, constants.mouse_size, constants.mouse_pointer_drag)
		self.mouse_sprite_drag = Sprite(self.mouse_component_drag)

		# by default the mouse pointer will be a normal pointer and not a "drag and drop" pointer
		self.mouse_sprite = self.mouse_sprite_pointer

		# to ensure that only one sound at a time can be played on a page
		self.playing_channel = None
		self.object_being_heard = None

		# by default, the language textbox is not enabled
		self.language_image = None

		# by default, no text legend shown below
		self.legend_text_component = None

		self.legend_text_pos = constants.legend_text_pos
		self.legend_text_size = constants.legend_text_size

		self.legend_text_color_index = 0

		self.update()

	def init_country_flags(self) :
		# init of official languages flag stuff
		self.countries = common.randomize_list(copy.copy(i18n.countries[self.language]))
		self.country_index = 0
		if (self.globalvars.user_country != None) :
			if (self.globalvars.user_country in self.countries) :
				# in case the user set up his country in locale, we will start the flag animation with its country
				self.country_index = self.countries.index(self.globalvars.user_country)
								
		self.country_ticks = 0


	def append(self, item) :
		self.items.append(item)

	def listen_to_mouse_over(self, item) :
		self.items_listen_mouse_over.append(item)
		
	def append_back(self, item) :
		self.items_back.append(item)
	
	def remove(self, item) :

		if (item in self.items_listen_mouse_over) :
			self.items_listen_mouse_over.remove(item)

		dirty_rect = item.erase()
		
		self.items.remove(item)
		
		return dirty_rect	
		
	def remove_all(self) :
		self.legend_text_component = None
		self.items = []
		self.items_back = []
		self.items_listen_mouse_over = []
			
		
	def update(self) :
		self.rect = Rect((0,0),(self.screen.get_width(), self.screen.get_height()))
			
		for item_back in self.items_back :	
			item_back.update()
		
		self.draw_back()					
		
		for item in self.items :
			item.update()
			
	
	def draw_back(self) :
		
		if ((self.background_file != None) and (self.background == None)) :
			(self.background, foo) = load_image(self.background_file, (self.screen.get_width(), self.screen.get_height()), self.background_mode, self) 
		
			# in case the image is smaller than the screen
			# center the background to fit the screen
			if ((self.background.get_width() != self.screen.get_width()) or (self.background.get_height() != self.screen.get_height())) : 
				self.big_background = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
				
				self.big_background.blit(self.background, ((self.screen.get_width()-self.background.get_width())/2,(self.screen.get_height()-self.background.get_height())/2))
				
				self.background = self.big_background
			
			# remove any alpha which could be set on the background
			self.background.convert()
			
		# not very clean
		# we pretend the page surface is the background
		# so we will draw directly to the background
		save_screen = self.screen
		self.screen = self.background
		
		for item_back in self.items_back :
			item_back.draw()
		
		# again clean situation
		self.screen = save_screen		

		if (self.background != None) :
			self.screen.blit(self.background, (0,0))
		
	def draw(self) :
		if (self.background != None) :
			self.screen.blit(self.background, (0,0))
		
		for item in self.items :
			item.draw()
		

	def was_something_clicked(self, (x, y), mousebutton) :
		# The idea is to check components which might have been clicked
		# starting from the last one which was drawn.
		# The last one drawn is "on top" and more visible
		# than eventual other items drawn before (and thus displayed "under")
		index = len(self.items)
	
		while (index > 0) :
			
			item = self.items[index - 1]
			
			if (item.rect.collidepoint(x,y) == True) :
				return item.was_clicked((x,y), mousebutton)
			
			index = index - 1
	
		return None

	def components_mouse_over(self, (x, y)) :
		# The idea is to check components were the mouse might be going over
		# starting from the last one which was drawn.
		# The last one drawn is "on top" and more visible
		# than eventual other items drawn before (and thus displayed "under")
		index = len(self.items_listen_mouse_over)
	
		while (index > 0) :
			
			item = self.items_listen_mouse_over[index - 1]
			
			if (item.rect.collidepoint(x,y) == True) :

				if (self.last_mouse_over != item) :
					# new mouse over
					self.last_mouse_over = item
					return (item, self.last_mouse_over)

				else :
					# no changes = mouse over + mouse still pointing on the object
					return (None, None)
			
			index = index - 1

		# here the mouse had left the previously mouse overed component

		mouse_over_ended = self.last_mouse_over

		self.last_mouse_over = None
	
		return (None, mouse_over_ended)
		
	def key_pressed(self, unicode_val, key, mod) :
		
		if (self.activated_component != None) :
			return self.activated_component.key_pressed(unicode_val, key, mod)
		else :
			return []		
		
	def activate(self, component) :
		# this method 'activates' a component in the page (gives the focus)
		if (self.activated_component == component) :
			# this is another click an on already activated textbox
			# => nothing to do
			return []
		
		dirty_rect = self.desactivate()
			
		self.activated_component = component
		
		return dirty_rect + component.activate()
		
	def desactivate(self) :
		# this methods desactivates an eventual active component
		# in the page (it looses the focus)
		
		if (self.activated_component != None) :
			# if there was another component receiving key events
			# we make it back to normal state
			dirty_rect = self.activated_component.desactivate()
		
			self.activated_component = None
			
			return dirty_rect
		else :
			return []
		

	def append_sprite(self, sprite) :
		self.sprites.append(sprite)
		
		return sprite
	
	def remove_sprite(self, sprite) :
		self.sprites.remove(sprite)
		
	
	def record_background_sprites(self) :
		for sprite in self.sprites :
			sprite.record_background()
			
	def erase_sprites(self) :
		dirty_rects = []
		
		for sprite in self.sprites :
			dirty_rects = dirty_rects + sprite.erase()

		dirty_rects = dirty_rects + self.mouse_sprite.erase()
	
		return dirty_rects
	
	def set_dragged_sprite(self, sprite, (mouse_x, mouse_y) = (0, 0)) :

		if (sprite != None) :

			(component_x, component_y) = (sprite.component.rect.centerx, sprite.component.rect.centery)
			(mouse_delta_x, mouse_delta_y) = (mouse_x - component_x, mouse_y - component_y)

			self.dragged_delta = (mouse_delta_x, mouse_delta_y)

			self.append_sprite(sprite)

		else :
			if (self.dragged_sprite != None) :
				self.remove_sprite(self.dragged_sprite)

		self.dragged_sprite = sprite



	
	def draw_sprites(self) :
		
		if (self.dragged_sprite != None) :
			
			component = self.dragged_sprite.component

			(drag_x, drag_y) = pygame.mouse.get_pos()
			
			(delta_x, delta_y) = self.dragged_delta

			(drag_x, drag_y) = (drag_x - delta_x, drag_y - delta_y)

			component.rect.center = (drag_x, drag_y)		
			
			if (component.__class__  == TextBox) :

				component.text_component.rect.center = (drag_x, drag_y)
				component.box_component.rect.center = (drag_x, drag_y)

		# custom mouse pointer management
		if (self.mouse_sprite != None) :
			
			if ((self.dragged_sprite == None) and (self.mouse_sprite != self.mouse_sprite_pointer)) :
				# switch to "normal" mouse pointer

				self.mouse_sprite = self.mouse_sprite_pointer

			elif ((self.dragged_sprite != None) and (self.mouse_sprite == self.mouse_sprite_pointer)) :
				# switch to "drag and drop" mouse pointer

				self.mouse_sprite = self.mouse_sprite_drag

		
			# TODO : implement hot spot !

			self.mouse_sprite.component.rect.topleft = pygame.mouse.get_pos()			

			
		dirty_rects = []
		
		for sprite in self.sprites :
			
			sprite.record_background()

		self.mouse_sprite.record_background()

		
		for sprite in self.sprites :
		
			dirty_rects = dirty_rects + sprite.component.draw()

		dirty_rects = dirty_rects + self.mouse_sprite.component.draw()

	
		return dirty_rects
	
	def animate(self) :
		# this is a method which can be called at each frame of the game
		# can be used to animate or refresh some objects
		# by default, it does nothing
		# you have to define it into a subclass 
		return None
		
		
	def x_pc2px(self, x_percent) :
		# converts x coordinates in percents into pixels
		return (round((x_percent * self.screen.get_width()) / 100, 0))
	
	def y_pc2px(self, y_percent) :
		# converts y coordinates in percents into pixels
		return (round((y_percent * self.screen.get_height()) / 100, 0))
		

	def x_px2pc(self, x) :
		# converts x coordinates in pixels into percents
		return ((x * 100.0) / self.screen.get_width())
	
	def y_px2pc(self, y) :
		# converts y coordinates in pixels into percents
		return ((y * 100.0) / self.screen.get_height())

	def fade_out(self) :
		# turns the page into black
		
		##clock = pygame.time.Clock()
		
		##for alpha in range(4) :
			
		box = Box(self, (0, 0), (100, 100), (0, 0, 0), 180)
		box.draw()
	
		pygame.display.flip()
			
		##	clock.tick(constants.framerate)
			
	def fade_in(self) :
		
		clock = pygame.time.Clock()
		
		## for alpha in range(4) :
		
		self.draw()
		
		##	box = Box(self, (0, 0), (100, 100), (0, 0, 0), 80*(4-alpha))
		##	box.draw()
	
		pygame.display.flip()
			
		##	clock.tick(constants.framerate)			
			
		## self.draw()
		## pygame.display.flip()
	
	def can_play_sound(self, object_to_hear) :
		# returns true if it is possible to play a sound 
		# (ie no sound being played at the moment, or different objects requesting to be "heard")
		
		can_play_sound = True
		
		if (self.playing_channel != None) :
			if ((self.playing_channel.get_busy() == True) and (self.object_being_heard == object_to_hear)) :
				can_play_sound = False

		return can_play_sound

	def play_congratulations_sound(self) :

		congratulations_sounds = []

		if (self.globalvars.congrats_sounds_active == True) :
			congratulations_sounds = congratulations_sounds + i18n.sound[1000]

		if (self.globalvars.congrats_voices_active == True) :
			congratulations_sounds = congratulations_sounds + i18n.voice[self.language][1000]



		if (self.can_play_sound(self) == True) :
			if (len(congratulations_sounds) > 0) :
				self.play_sound(congratulations_sounds[random.randint(0, len(congratulations_sounds) -1 ) ], self)



	def play_error_sound(self) :

		error_sounds = []

		if (self.globalvars.congrats_sounds_active == True) :
			error_sounds = error_sounds + i18n.sound[1001]

		if (self.globalvars.congrats_voices_active == True) :
			error_sounds = error_sounds + i18n.voice[self.language][1001]


		if (self.can_play_sound(self) == True) :
			if (len(error_sounds) > 0) :
				self.play_sound(error_sounds[random.randint(0, len(error_sounds) -1 ) ], self)


	def play_sound(self, sound_filename, object_to_hear) :

		sound_filename = common.find_file(sound_filename, self.globalvars)

		if (os.path.exists(sound_filename) == False) :
			common.warn("File "+sound_filename+" does not exist")
			
			return None
		else :
			sound = pygame.mixer.Sound(sound_filename)
			channel = sound.play()
		
			self.playing_channel = channel

			self.object_being_heard = object_to_hear

	def next_country(self) :
		# will change the country flag inside a language textbox

		if (self.language_image != None) :
			self.country_ticks = self.country_ticks + 1

			if (self.country_ticks >= constants.country_ticks_for_animation) :

				dirty_rects = self.language_image.erase()

				self.country_ticks = 0

				self.country_index = self.country_index + 1

				if (self.country_index >= len(self.countries)) :
					self.country_index = 0

				self.language_image.image_file = i18n.countries_prefix + self.countries[self.country_index] + i18n.countries_suffix

				self.language_image.update()

				self.language_image.outline(constants.flag_outline_color, constants.flag_outline_width)

				dirty_rects = dirty_rects + self.language_image.draw()

				return dirty_rects

			else :
				return []

	def add_legend_text(self, component) :


		if ((component.associated_text != None) and (component.associated_text_color != None)) :

			self.legend_text_component = Text(self, component.associated_text, self.legend_text_pos, self.legend_text_size, self.fonts, component.associated_text_color, 1)
		
			self.append(self.legend_text_component)

			return (self.legend_text_component.draw())

		else :
			return []

	def remove_legend_text(self) :
		if (self.legend_text_component != None) :

			dirty_rects = self.remove(self.legend_text_component)

			self.legend_text_component = None

			return dirty_rects

		else :
			return []





class Game_Page(Page) :

	def __init__(self, globalvars, game) :

		self.game = game

		if (len(self.game.backgrounds) > 0) :
			(background_file, background_mode) = self.game.backgrounds[random.randint(0, len(self.game.backgrounds)-1)]
		else :
			(background_file, background_mode) = (constants.background_file[self.game.game_type], constants.background_mode[self.game.game_type])

		Page.__init__(self, globalvars, background_file, background_mode)

		# arcade stuff
		self.timer_text = None
		self.score_text = None

		self.init_game_components()


	def init_game_components(self) :
		# add standard objects for the game


		self.init_country_flags()

		if (self.game.score.get_arcade_mode() == True) :
			title_pos = (1, 1)
			title_size = (49, 5)

			title_box_color = (0, 0, 0)
			title_box_alpha = 0


			self.append_back(Box(self, (0, 0), (100, 7)))

		else :
			title_pos = (5, 1)
			title_size = (90, 5)

			title_box_alpha = constants.box_alpha
			title_box_color = constants.box_color



		# title of the game at the top of the screen
		self.append(TextBox(self, self.game.get_title(self.language), title_pos, title_size, self.fonts, constants.text_color, 11, i18n.countries_prefix + self.countries[self.country_index] + i18n.countries_suffix, title_box_alpha, title_box_color))

		# quit icon
		self.quit_icon = Image(self, constants.stop_icon_pos, constants.stop_icon_size, constants.stop_icon)

		self.append(self.quit_icon)

		# "next" icon
		self.next_icon = Image(self, constants.go_next_icon_pos, constants.go_next_icon_size, constants.go_next_icon)

		if (self.game.score.get_arcade_mode() == True) :


			if (self.game.score.count_good == True) :
				self.score_good_text = Text(self, self.game.score.good_answers_toString(), constants.score_good_pos, constants.score_good_size, self.fonts, constants.text_color, 2)

				self.append(self.score_good_text)

				self.append_back(Image(self, constants.score_good_icon_pos, constants.score_good_icon_size, constants.score_good_icon))



			if (self.game.score.count_wrong == True) :
				self.score_wrong_text = Text(self, self.game.score.wrong_answers_toString(), constants.score_wrong_pos, constants.score_wrong_size, self.fonts, constants.text_color, 2)

				self.append(self.score_wrong_text)

				self.append_back(Image(self, constants.score_wrong_icon_pos, constants.score_wrong_icon_size, constants.score_wrong_icon))



			if (self.game.score.record_time == True) :
				self.timer_text = Text(self, self.game.score.timer.toString(), constants.timer_pos, constants.timer_size, self.fonts, constants.text_color, 2)

				self.append(self.timer_text)

				self.append_back(Image(self, constants.timer_icon_pos, constants.timer_icon_size, constants.timer_icon))


			self.draw_back()


		
	def draw_arcade(self) :

		dirty_rects = []

		if (self.game.score.get_arcade_mode() == True) :


			if (self.game.score.count_good == True) :
				# good answers
				score_good = self.game.score.good_answers_toString()

				if (cmp(self.score_good_text.text, score_good) != 0) :

					self.score_good_text.erase()
					self.score_good_text.set_text(score_good)

					dirty_rects = dirty_rects + self.score_good_text.draw()


			if (self.game.score.count_wrong == True) :
				# wrong answers
				score_wrong = self.game.score.wrong_answers_toString()

				if (cmp(self.score_wrong_text.text, score_wrong) != 0) :

					self.score_wrong_text.erase()
					self.score_wrong_text.set_text(score_wrong)

					dirty_rects = dirty_rects + self.score_wrong_text.draw()


			if (self.game.score.record_time == True) :
				# timer

				timer_to_string = self.game.score.timer.toString()

				if (cmp(self.timer_text.text, timer_to_string) != 0) :
					# we draw again only if the timer value changed

					self.timer_text.erase()
					self.timer_text.set_text(timer_to_string)

					dirty_rects = dirty_rects + self.timer_text.draw()


		return dirty_rects




		
class Fonts() :
	# This object caches the various fonts which will be used in the game
		
	default_font = None	
		
	def __init__(self, font_file) :
		
		self.font_file = font_file
		
		# here, we temporarily load the font to store the ratio ascent/descent
		font = pygame.font.Font(font_file, 100)
		
		self.ascent = font.get_ascent()
		self.descent = -font.get_descent()
		
		Fonts.default_font = self # not very clean...
		
		
		
		
	def get_font(self, page, height_percent) :
		# returns a Font object which takes height_percent of the screen
			
		font_height = (page.screen.get_height() * height_percent)/100.0	
			
		font_height = (font_height * 100.0) // (self.ascent + self.descent)
		
		return pygame.font.Font(self.font_file, int(font_height))
		
			
class Base() :
	# the base class for the graphical components
	# it mutualizes some common features of those objects
	
	def __init__(self, page, (x_percent, y_percent), (width_percent, height_percent)) :

		self.x_percent = x_percent
		self.y_percent = y_percent
		self.width_percent = width_percent
		self.height_percent = height_percent


		self.original_x_percent = x_percent
		self.original_y_percent = y_percent
		self.original_width_percent = width_percent
		self.original_height_percent = height_percent

		self.associated_text = ""
		self.associated_text_color = None

		self.init_absolute(page)

		
	def init_absolute(self, page) :
		# this method is called also for 'non percent objects'
		self.page = page
		
		# no clipping by default
		self.cliprect = None # clipping in percent
		self.cliprect_abs = None # absolute clipping
	
		# no associated object by default
		self.associated_object = None
		
		# no associated sounds by default
		self.associated_sounds = []
		
	def play_random_associated_sound(self) :
		if (len(self.associated_sounds) > 0) :
				
			if (self.page.can_play_sound(self) == True) :

				random_sound = self.associated_sounds[random.randint(0, len(self.associated_sounds)-1)]
					
				self.page.play_sound(random_sound, self)
				
		
		
	def set_associated_object(self, object) :
		self.associated_object = object

	def set_associated_text(self, text) :
		self.associated_text = text
		
		self.page.legend_text_color_index = self.page.legend_text_color_index + 1

		if (self.page.legend_text_color_index >= len(constants.legend_text_colors)) :
			self.page.legend_text_color_index = 0

		self.associated_text_color = constants.legend_text_colors[self.page.legend_text_color_index]

	
	def set_cliprect(self, ((x_percent, y_percent), (width_percent, height_percent))) :
		self.cliprect = ((x_percent, y_percent), (width_percent, height_percent))

	def set_center_abs(self, (x,y)) :
		self.rect.center = (x, y)

		x_center_percent = self.page.x_px2pc(x)
		y_center_percent = self.page.y_px2pc(y)

		self.x_percent = x_center_percent - (self.width_percent / 2.0)
		self.y_percent = y_center_percent - (self.height_percent / 2.0)

	
	def update(self) :
		self.rect = Rect(((self.x_percent*self.page.screen.get_width())/100, (self.y_percent*self.page.screen.get_height())/100), ((self.width_percent*self.page.screen.get_width())/100, (self.height_percent*self.page.screen.get_height())/100))
	
	def erase(self) :
		dirty_rect = self.rect
		
		# first, we reset to the background
		self.page.screen.blit(self.page.background.subsurface(self.rect.clip(self.page.screen.get_clip())), self.rect.clip(self.page.screen.get_clip()))
		
		# and then, we look for eventual other objects to redraw
		for item in self.page.items :
			if (item.rect.colliderect(self.rect)) :
				if (item != self) :
					old_cliprect_abs = item.cliprect_abs
					item.cliprect_abs = self.rect
					item.draw()
					item.cliprect_abs = old_cliprect_abs
				
		
		
		return [copy.copy(dirty_rect)]
	
	def draw(self) :
		
		cut_rect = self.cliprect_abs
		
		if (cut_rect == None) :
			if (self.cliprect != None) :
				((x_percent, y_percent), (width_percent, height_percent)) = self.cliprect
				cut_rect = Rect((x_percent*self.page.screen.get_width())/100, \
				(y_percent*self.page.screen.get_height())/100, \
				(width_percent*self.page.screen.get_width())/100, \
				(height_percent*self.page.screen.get_height())/100)			
		
		
		if (cut_rect == None) :
			return([self.page.screen.blit(self.surface, self.rect)])
		else :
			if (self.rect.colliderect(cut_rect) == True) :
				common_rect = self.rect.clip(cut_rect)
				area_rect = copy.copy(common_rect)
				area_rect.topleft=(common_rect.left-self.rect.left, common_rect.top-self.rect.top)
				
				return [(self.page.screen.blit(self.surface, common_rect, area_rect))]
			else :
				return []
	
	def move_delta(self, (delta_x, delta_y)) :
		
		self.rect.left = self.rect.left + delta_x
		self.rect.top = self.rect.top + delta_y
	
	def was_clicked(self, (x, y), mousebutton) :
		return (self, self.associated_object, [])
	

	def get_text(self) :
		return ""


	def outline(self, color, thickness) :
		rect = copy.copy(self.rect)

		rect.topleft=(0,0)

		pygame.draw.rect(self.surface, color, rect, thickness)	

	def get_original_rect(self) :
		return Rect(self.page.x_pc2px(self.original_x_percent),
			self.page.y_pc2px(self.original_y_percent),
			self.page.x_pc2px(self.original_width_percent),
			self.page.y_pc2px(self.original_height_percent))

		
class TextBox(Base) :		
			
	def __init__(self, page, text, (x_percent, y_percent), (width_percent, height_percent), fonts, text_color, align, image_file = None, alpha = constants.box_alpha, box_color = constants.box_color) :
		# page : page where the TextBox will be drawn	
		# text : text to display	
			
		Base.__init__(self, page, (x_percent, y_percent), (width_percent, height_percent))
		
		self.fonts = fonts
		self.text_color = text_color
		self.align = align
		self.draw_box = True # by default, a background box is displayed under the text		
		self.box_color = box_color
		

		self.text = text
		self.image_file = image_file
		
		self.image_component = None
		
		self.alpha = alpha
		
		self.update()
		
	def set_text(self, text) :
		# NB : this method should not be used in case of a shrinked text box
		# because it does not update the box
		self.text = text
		self.text_component.set_text(text)
		
	def get_text(self) :
		return self.text_component.text	
		
		
	def update(self) :
		
				
		# align values :
		#               0 = left aligned
		#               1 = centered
		#               2 = right aligned
		#               11 = centered, shrinking width of box to fit text if possible
		#		12 = right aligned with shrinking
		self.text_component = Text(self.page, self.text, (self.x_percent, self.y_percent), (self.width_percent, self.height_percent), self.fonts, self.text_color, self.align)		
		
		self.x_percent_new = self.x_percent
		self.width_percent_new = self.width_percent
		
		if (self.align >= 10) :
			# potential shrinking of box to fit text
			shrink_x = ((self.width_percent * self.page.screen.get_width()) / 100) - self.text_component.surface.get_width()

			if (shrink_x > 0) :
				
				if (self.align == 11) :
					self.x_percent_new = self.x_percent + ((100.0*shrink_x)/(self.page.screen.get_width()*2.0))
				elif (self.align == 12) :
					self.x_percent_new = self.x_percent + ((100.0*shrink_x)/self.page.screen.get_width())
				
				self.width_percent_new = (self.text_component.rect.width * 100.0) / self.page.screen.get_width()
		
		width_image_percent = 0.0
		
		if (self.image_file != None) :
			
			height_image_percent = (self.height_percent * constants.image_in_textbox_ratio)
			delta_image_y_percent = (self.height_percent * (1.0 - constants.image_in_textbox_ratio)) / 2.0
			
			width_image_percent = self.height_percent
			
			self.image_component = Image(self.page, (self.x_percent_new - width_image_percent / 2.0, self.y_percent + delta_image_y_percent), (width_image_percent, height_image_percent), self.image_file)
		
			# "grow up" a bit the image on the x axis
			# to allow for margins around the pic
			# NB: grows because image_in_textbox_ratio < 1
			width_image_percent = width_image_percent / constants.image_in_textbox_ratio
		
			if (self.align >= 10) :
				# positioning of the text was done before...
				# we have to "push" the text to let some space for the picture
				self.text_component.rect.left = self.text_component.rect.left + ((width_image_percent * self.page.screen.get_width()) / 200.0)
		
		
		self.box_component = Rounded_Box(self.page, (self.x_percent_new - (width_image_percent / 2.0), self.y_percent), (self.width_percent_new + width_image_percent, self.height_percent), self.box_color, self.alpha)
		

		self.rect = self.box_component.rect
			
			
	def draw(self) :

		self.box_component.draw()
		
		self.text_component.draw()
		
		if (self.image_component != None) :
			self.image_component.draw()
		
		return [self.box_component.rect]
	
	
	def was_clicked(self, (x, y), mousebutton) :

		retval = Base.was_clicked(self, (x,y), mousebutton)
		return retval

	def move_delta(self, (delta_x, delta_y)) :
		if (self.box_component != None) :
			self.box_component.move_delta((delta_x, delta_y))
		if (self.image_component != None) :		
			self.image_component.move_delta((delta_x, delta_y))
		if (self.text_component != None) :		
			self.text_component.move_delta((delta_x, delta_y))
			
		self.rect = self.box_component.rect
		
	def set_cliprect(self, area_scrolled_percent) :
	
		if (self.box_component != None) :
			self.box_component.set_cliprect(area_scrolled_percent)
		if (self.image_component != None) :		
			self.image_component.set_cliprect(area_scrolled_percent)
		if (self.text_component != None) :		
			self.text_component.set_cliprect(area_scrolled_percent)
		
		Base.set_cliprect(self, area_scrolled_percent)
		

class Image(Base) :
	def __init__(self, page, (x_percent, y_percent), (width_percent, height_percent), image_file,  alpha = 255, size_ratio_percent = 100, mode = "CENTERED") :

		new_width_percent = (width_percent * size_ratio_percent) / 100.0
		new_height_percent = (height_percent * size_ratio_percent) / 100.0
		x_percent = x_percent + ((width_percent - new_width_percent) / 2.0)
		y_percent = y_percent + ((height_percent - new_height_percent) / 2.0)
		
		Base.__init__(self, page, (x_percent, y_percent), (new_width_percent, new_height_percent))

		self.image_file = image_file			
		self.alpha = alpha	
		self.mode = mode

		self.masked_surface = None
		self.original_surface = None

		self.update()			
	
	def update(self) :
	
		max_width = int(round((self.width_percent * self.page.screen.get_width()) / 100.0))
		max_height = int(round((self.height_percent * self.page.screen.get_height()) / 100.0))

		(self.surface, self.original_size) = load_image(self.image_file, (max_width, max_height), self.mode, self.page)

		if (self.alpha != 255) :
			
			self.surface.set_alpha(self.alpha)
			self.surface = self.surface.convert_alpha()
		
		self.x = int(round((self.x_percent * self.page.screen.get_width()) / 100.0))
		self.y = int(round((self.y_percent * self.page.screen.get_height()) / 100.0))


		if (cmp(self.mode, "CENTERED") == 0) :
			self.x = self.x + ((max_width - self.surface.get_width()) / 2)
			self.y = self.y + ((max_height - self.surface.get_height()) / 2)
		elif (cmp(self.mode, "BOTTOMLEFT") == 0) :
			self.y = self.y + (max_height - self.surface.get_height())
				
		self.rect = Rect((self.x, self.y), (self.surface.get_width(), self.surface.get_height()))

		self.original_surface = self.surface


	def compute_masked_surface(self, pattern_filename) :

		(pattern_surface, foo) = load_image(pattern_filename, self.rect.size, "FILL", self.page)
				
		self.masked_surface = pygame.surface.Surface(self.rect.size, SRCALPHA)

		pxarray_org = pygame.PixelArray(self.surface)
		pxarray_masked = pygame.PixelArray(self.masked_surface)
		pxarray_pattern = pygame.PixelArray(pattern_surface.convert_alpha())

		for x in range(self.masked_surface.get_width()) :
			for y in range(self.masked_surface.get_height()) :
				if (pygame.Color(pxarray_org[x][y]).a != 0) :
					pxarray_masked[x][y] = pygame.Color(pxarray_pattern[x][y])


	def mask_surface(self) :
		self.surface = self.masked_surface

	def unmask_surface(self) :
		self.surface = self.original_surface



		
class Image_Absolute(Image) :
		
	def __init__(self, page, (x, y), (width, height), surface) :
		
		Base.init_absolute(self, page)
		
		self.rect = Rect((x, y), (width, height))
		
		self.surface = surface		

	
		
class Text(Base) :
	def __init__(self, page, text, (x_percent, y_percent), (width_percent, height_percent), fonts, color, align) :
		# values for align :
		#               0 = left aligned
		#               1 = centered
		#               2 = right aligned
		# 		11 = like 1, used when called from a 'shrunk' textbox	

		Base.__init__(self, page, (x_percent, y_percent), (width_percent, height_percent))
		
		self.text = text		
		
		self.fonts = fonts		
		self.color = color
		
		self.align = align
		if (self.align >= 10) :
			self.align = self.align - 10
		
		self.cliprect = None
		
		self.update()
		
	def set_text(self, text) :
		self.text = text
		self.update()

			
	def update(self) :
		self.x = (self.x_percent * self.page.screen.get_width()) / 100.0
		self.y = (self.y_percent * self.page.screen.get_height()) / 100.0		

		text_does_fit = False
		self.text_height_percent = self.height_percent
	
		while (text_does_fit == False) :
			# this loop shrinks the text until it fits in the allowed area
			self.font = self.fonts.get_font(self.page, self.text_height_percent)
					
			# we add spaces on left and right to look "nicer" inside shrunk boxes
			self.surface = self.font.render(u" "+self.text+u" ", True, self.color) 

			if (self.surface.get_width() > self.page.x_pc2px(self.width_percent)) :
				self.text_height_percent = self.text_height_percent - 0.25
			else :
				text_does_fit = True

			if (self.text_height_percent <= 0.25) :
				# this should not happen, but just in case, to avoid an infinite loop
				text_does_fit = True

		if (self.text_height_percent != self.height_percent) :
			# centering y axis in case the text had to be shrunk
			self.y = self.y + self.page.y_pc2px((self.height_percent - self.text_height_percent) / 2)

		
		if (self.align == 0) :
			self.text_x = 0	
		elif (self.align == 1) :
			self.text_x = ((self.width_percent*self.page.screen.get_width())/200.0) - (self.surface.get_width() / 2.0)
		else :
			self.text_x = (self.width_percent*self.page.screen.get_width())/100.0 - self.surface.get_width()
					
		self.x = self.x + self.text_x
		
		self.rect = Rect((self.x, self.y), (self.surface.get_width(), self.surface.get_height()))
	
		
class Box(Base) :
		
	def __init__(self, page, (x_percent, y_percent), (width_percent, height_percent), color = constants.box_color, alpha = constants.box_alpha) :
		
		Base.__init__(self, page, (x_percent, y_percent), (width_percent, height_percent))

		self.color = color
		self.alpha = alpha
		
		self.update()
		
	def update(self) :
		
		Base.update(self)	
		
		self.surface = pygame.Surface((self.rect.width, self.rect.height))
		self.surface.fill(self.color)
	
		self.surface.set_alpha(self.alpha)	


class Empty_Box_Absolute(Box) :
	
	def __init__(self, page, (x, y), (width, height), color, alpha) :
		
		Base.init_absolute(self, page)
		
		self.rect = Rect((x, y), (width, height))
		
		self.color = color
		self.alpha = alpha
		
		self.update()
		
	def update(self) :	
		
		self.surface = pygame.Surface((self.rect.width, self.rect.height), 0, self.page.screen)
		
		pygame.draw.rect(self.surface, self.color, Rect((0,0), (self.rect.width, self.rect.height)) , 1)
	
		self.surface.set_alpha(self.alpha)		
	
	

class Rounded_Box(Box) :
	
	def update(self) :
		Box.update(self)
		
		self.surface.set_colorkey(constants.transparent_color)
		
		# make corners a bit round
		self.surface.set_at((0,0), constants.transparent_color)
		self.surface.set_at((0,1), constants.transparent_color)
		self.surface.set_at((1,0), constants.transparent_color)
		
		self.surface.set_at((self.rect.width-1,0), constants.transparent_color)
		self.surface.set_at((self.rect.width-2,0), constants.transparent_color)
		self.surface.set_at((self.rect.width-1,1), constants.transparent_color)
		
		self.surface.set_at((0,self.rect.height-1), constants.transparent_color)
		self.surface.set_at((1,self.rect.height-1), constants.transparent_color)
		self.surface.set_at((0,self.rect.height-2), constants.transparent_color)
		
		self.surface.set_at((self.rect.width-1,self.rect.height-1), constants.transparent_color)
		self.surface.set_at((self.rect.width-2,self.rect.height-1), constants.transparent_color)
		self.surface.set_at((self.rect.width-1,self.rect.height-2), constants.transparent_color)		



class ScrollArea(Base) :
	
	# TODO #
	# add a lift between the arrows
	
	# TODO #
	# implement horizontal scrolling
	
	def __init__(self, page, (x_percent, y_percent), (width_percent, height_percent), width_scrollbar_percent, scroll_step_percent) :
		
		Base.__init__(self, page, (x_percent, y_percent), (width_percent, height_percent))

		self.area_scrolled_percent = ((x_percent, y_percent), (width_percent - width_scrollbar_percent, height_percent))

		self.width_scrollbar_percent = width_scrollbar_percent

		self.scroll_step_percent = scroll_step_percent

		self.items = []

		self.update()
		
	def update(self) :
		
		Base.update(self)
		
		self.scroll_step = round((self.scroll_step_percent*self.page.screen.get_height()) / 100.0, 0)
		
		if (self.scroll_step < 1) :
			# just in case
			self.scroll_step = 1
		
		((x_percent, y_percent), (width_percent, height_percent)) = self.area_scrolled_percent	
			
		self.arrow_up_component = Image(self.page, (x_percent + width_percent, self.y_percent), (self.width_scrollbar_percent, self.width_scrollbar_percent), constants.icon_arrow_up)
		
		self.arrow_down_component = Image(self.page, (x_percent + width_percent, self.y_percent+self.height_percent-self.width_scrollbar_percent), (self.width_scrollbar_percent, self.width_scrollbar_percent), constants.icon_arrow_down)
		
		self.area_scrolled = Rect((x_percent*self.page.screen.get_width())/100.0, \
			(y_percent*self.page.screen.get_height())/100.0, \
			(width_percent*self.page.screen.get_width())/100.0, \
			(height_percent*self.page.screen.get_height())/100.0)

		for item in self.items :
			item.update()

	def append(self, item) :
		item.set_cliprect(self.area_scrolled_percent)
		
		self.items.append(item)		

		
	def was_clicked(self, (x, y), mousebutton) :
		
		# TODO #
		# transformation of an eventual 'wheel down' from the mouse
		# into a click on the arrow down of a scrollbar	
		
		
		if (len(self.items) > 0) :
			# we start to look for selection or click on an arrow only
			# if the list of items is not empty
		
			# this part is checking if the arrows were used
			delta = 0	
			if (self.arrow_down_component.rect.collidepoint(x,y) == True) :
				delta = -self.scroll_step
				
				if (self.items[-1].rect.bottom + delta < self.rect.bottom) :
					delta = self.rect.bottom - self.items[-1].rect.bottom
					
			elif (self.arrow_up_component.rect.collidepoint(x,y) == True) :
				delta = self.scroll_step

				if (self.items[0].rect.top + delta > self.rect.top) :
					delta = self.rect.top - self.items[0].rect.top 
					
			if (delta != 0) :
				if (self.items[-1].rect.bottom - self.items[0].rect.top > self.rect.height) :
					# we will scroll only if the list of items is bigger than
					# the scrollarea
					for item in self.items :
						item.move_delta((0, delta))
								
					self.erase()
###					self.background_box_component.draw()
					self.draw()				
					return (self, None, [self.rect])
			
			# now we check whether some entry was clicked
			for item in self.items :
				if (item.rect.collidepoint(x,y) == True) :
					return item.was_clicked((x, y), mousebutton)

		return None
		
	def draw(self) :
	
		self.arrow_up_component.draw()
		self.arrow_down_component.draw()
		
		for item in self.items :
			item.draw()
	
		return [self.rect]




def get_image_info(file, globalvars = None) :
	
	file = common.find_file(file, globalvars)
	
	file_info = gtk.gdk.pixbuf_get_file_info(file)
	
	if (file_info != None) :
	
		(image_type, width, height) = file_info
	
		return (image_type, width, height)
	
	else :
		common.warn("Unable to get file information for file "+file)
		
		return (None, None, None)


def load_image(file, (desired_width, desired_height) = (0, 0), mode = "CENTERED", page = None) :
	
	# possible modes =
	# CENTERED : as big as possible, keeping width/height ratio
	# BOTTOMLEFT : as big as possible, keeping width/height ratio, image starts at the bottom left
	# TOPLEFT : as big as possible, keeping width/height ratio, image starts at the top left
	# FILL : use all the desired_width and desired_height. Eventually changing the width/height ratio


	(desired_width, desired_height) = (int(round(desired_width)), int(round(desired_height)))


	if ((cmp(mode, "TOPLEFT") == 0) or (cmp(mode, "BOTTOMLEFT") == 0)) :
		mode = "CENTERED"
	
	if (page != None) :
		globalvars = page.globalvars
	else :
		globalvars = None

	file = common.find_file(file, globalvars)
	
	(image_type, width, height) = get_image_info(file)
	
	if (image_type == None) :
		# probably file not found

		(image_type, width, height) = get_image_info(constants.missing_image)

		bitmap = pygame.image.load(common.find_file(constants.missing_image))
		
		if ((desired_width != 0) and (desired_height != 0)) :
			bitmap = pygame.transform.scale(bitmap, (desired_width, desired_height))
			
	elif (cmp(image_type["name"], "svg") == 0) :
		# we have an svg file to load
		
		if ((desired_width != 0) and (desired_height != 0)) :
			if (cmp(mode, "CENTERED") == 0)  :
				# centered mode = keep width/height ratio
				buf = gtk.gdk.pixbuf_new_from_file_at_size(file, desired_width, desired_height)
			else :
				# fill mode = do not keep width/height ratio, use all desired_width and desired_height
				loader = gtk.gdk.PixbufLoader()
				loader.set_size(desired_width, desired_height)
				
				svg_file_handler = open(file, 'rb')
				svg_data = svg_file_handler.read()
				svg_file_handler.close()
				
				loader.write(svg_data)
				loader.close()	
				

				buf = loader.get_pixbuf()



		else :
			buf = gtk.gdk.pixbuf_new_from_file(file)
			
			
		new_width = buf.get_width()
		new_height = buf.get_height()

		if (buf.get_bits_per_sample() != 8) :
			common.warn("SVG loading : the buffer should be made of 8 bits RGBA values !")

		string = buf.get_pixels()
		
		bitmap = pygame.image.fromstring(string, (new_width, new_height), "RGBA")
				
	else :		
		# we're loading a bitmap image

		bitmap = pygame.image.load(file)

		if ((desired_width != 0) and (desired_height != 0)) :
	
			if (cmp(mode, "CENTERED") == 0):

				bitmap = resize_image(bitmap, (desired_width, desired_height))
			else :
				bitmap = pygame.transform.scale(bitmap, (desired_width, desired_height))


	if bitmap.get_alpha() is None:
		bitmap = bitmap.convert()
	else:
		bitmap = bitmap.convert_alpha()	

	# returns the loaded bitmap
	# and its original dimensions (width, height) in the file
	return (bitmap, (width, height))



def resize_image(bitmap, (max_width, max_height)) :
	# this procedure resizes an image to use as much space as possible inside a
	# rectangle which has a size of (max_width, max_height)
	
	new_width = bitmap.get_width()
	new_height = bitmap.get_height()
	
	if ((new_width < max_width) and (new_height < max_height)) :
		# if both dimensions are smaller, we will grow the image
		
		if ((max_width / new_width) > (max_height / new_height)) :
			# the image could grow more on x than on y
			new_height = max_height
			if (new_height > constants.max_zoom * bitmap.get_height()) :
				new_height = constants.max_zoom * bitmap.get_height()
			
			new_width = (new_height * new_width) // bitmap.get_height()

		elif ((max_width / new_width) < (max_height / new_height)) :
			new_width = max_width
			if (new_width > constants.max_zoom * bitmap.get_width()) :
				new_width = constants.max_zoom * bitmap.get_width()				
			
			new_height = (new_width * new_height) // bitmap.get_width()

		else :
			# the image ratio is exactly the same as (max_width, max_height) ratio
			new_width = max_width
			new_height = max_height
		

	else :
		# we shrink the image
		if (new_width > max_width) :
			# we must keep proportions so we have to change the height...
			new_height = (new_height * max_width) // new_width
			new_width = max_width
				
		if (new_height > max_height) :
			# we must keep proportions so we have to change the width...
			new_width = (new_width * max_height) // new_height
			new_height = max_height	
	
	
	if ((new_width != bitmap.get_width()) or (new_height != bitmap.get_height)) :
		resized_bitmap = pygame.transform.scale(bitmap, (new_width, new_height))
		return resized_bitmap
	
	else :
		return bitmap


class Coordinates_converter() :
	# This objects allows coordinate conversion
	# between an initial Rect (eg: initial non resized image)
	# and a displayed Rect (image resized and placed on the screen)
	
	def __init__(self, page, initial_rect, new_rect) :
		
		self.page = page
		# page might be set to None if no 'percent' conversion is done

		self.initial_rect = initial_rect
		self.new_rect = new_rect
		
		self.x_ratio = (new_rect.width*1.0) / initial_rect.width
		self.y_ratio = (new_rect.height*1.0) / initial_rect.height
		
		self.x_delta = new_rect.left - initial_rect.left
		self.y_delta = new_rect.top - initial_rect.top
		
	def get_coords_px2pc(self, (x, y)) :
		# (x, y) are coordinates in the initial Rect, in pixels
		# returns (new_x_percent, new_y_percent) on the new Rect, in percent
		
		# scaling of coordinates
		new_x = (self.x_ratio * x)
		new_y = (self.y_ratio * y)
		
		# adding the deltas
		new_x = new_x + self.x_delta
		new_y = new_y + self.y_delta
		
		new_x_percent = (new_x*100.0) / self.page.screen.get_width()
		new_y_percent = (new_y*100.0) / self.page.screen.get_height()
		
		return(new_x_percent, new_y_percent)

	def get_size_px2pc(self, (width, height)) :
		# returns (new_width, new_height) on the new Rect, in percent
		
		# scaling of coordinates
		new_width = (self.x_ratio * width)
		new_height = (self.y_ratio * height)
		
		new_width_percent = (new_width*100.0) / self.page.screen.get_width()
		new_height_percent = (new_height*100.0) / self.page.screen.get_height()
		
		return(new_width_percent, new_height_percent)
	
	def get_coords_pc_org2pc(self, (x_percent_org, y_percent_org)) :
		# x_percent_org and y_percent_org are relative to the initial rect (and not to the whole page)
		
		x = (x_percent_org*self.initial_rect.width) / 100.0
		y = (y_percent_org*self.initial_rect.height) / 100.0
	
	
		return self.get_coords_px2pc((x, y))
		
	def get_size_pc_org2pc(self, (width_percent_org, height_percent_org)) :
		width = (width_percent_org*self.initial_rect.width) / 100.0
		height = (height_percent_org*self.initial_rect.height) / 100.0
	
		new_width = (self.x_ratio * width)
		new_height = (self.y_ratio * height)
		
		new_width_percent = self.page.x_px2pc(new_width)
		new_height_percent = self.page.y_px2pc(new_height)
		
		return(new_width_percent, new_height_percent)


	def get_coords_px_org2px(self, (x, y)) :
		# (x, y) are coordinates in the initial Rect, in pixels
		# returns (new_x, new_y) on the new Rect, in pixels
		

		# scaling of coordinates
		new_x = (self.x_ratio * x)
		new_y = (self.y_ratio * y)
		
		# adding the deltas
		new_x = new_x + self.x_delta
		new_y = new_y + self.y_delta
		
		return(new_x, new_y)


	def get_coords_px2px_org(self, (x, y)) :
		# (x, y) are coordinates in the new Rect, in pixels
		# returns (initial_x, intial_y) on the initial Rect, in pixels


		# TODO : remove this function because not used ?

		
		# scaling of coordinates
		initial_x = x / self.x_ratio 
		initial_y = y / self.y_ratio 
		
		initial_x = initial_x - self.x_delta
		initial_y = initial_y - self.y_delta
		
		return(initial_x, initial_y)

	def get_size_px_org2px(self, (width, height)) :
		# (width, height) are coordinates in the initial Rect, in pixels
		# returns (new_width, new_height) on the new Rect, in pixels
		
		# scaling of coordinates
		new_width = (self.x_ratio * width)
		new_height = (self.y_ratio * height)
		
		return(new_width, new_height)
