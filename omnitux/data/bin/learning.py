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

import pygame, random, copy
from pygame.locals import *
			
import ui, constants, xml_funcs, i18n, common, display_big


class Page_learning(ui.Game_Page) :

	# the idea is to click on all the displayed items
	#
	# two possible uses :
	# 1 - learn how to use the mouse and click somewhere
	# 2 - learn texts or sounds associated to images

	def __init__(self, game, globalvars) :

		
		self.dragged_sprite = None
		self.draggable_items = []

		# completed becomes True when all items have been clicked at least once
		self.completed = False
		

		ui.Game_Page.__init__(self, globalvars, game)

	
	def update(self) :
		
		ui.Page.update(self)


		# eventually adding text legend
		if (self.game.text_legend_area != None) :
			(self.legend_text_pos, self.legend_text_size) = self.game.text_legend_area


		# adding the items

		item_areas = copy.copy(self.game.item_areas)

		self.learning_cards_to_click = len(self.game.learning_cards_to_display)

		for learning_card in self.game.learning_cards_to_display :

			item_area = item_areas.pop()

			(pos, size) = item_area.get_pos_size()

			learning_card_image = ui.Image(self, pos, size, learning_card.image_filename)

			if (len(learning_card.sound_filenames) > 0) :
				learning_card_image.associated_sounds = learning_card.sound_filenames


			learning_card_image.compute_masked_surface("default/backgrounds/ABSTRACT-Pastel_1024x768.jpg")

			learning_card_image.mask_surface()

			learning_card_image.associated_object = learning_card

			self.append(learning_card_image)

			self.draggable_items.append(learning_card_image)


		self.draw_back()


	def was_something_clicked(self, (x, y), mousebutton) :
	
		clicked = ui.Page.was_something_clicked(self, (x,y), mousebutton)		
	
		if (clicked != None) :
			(component_clicked, foo, dirty1) = clicked	
			
			if ((self.dragged_sprite == None) and (mousebutton == 1)) :
				# this might be an item to drag 
				
				for draggable_item in self.draggable_items :
					
					if (component_clicked == draggable_item) :

						if (component_clicked.associated_object.clicked == False) :
							component_clicked.associated_object.clicked = True

							if (component_clicked.surface != component_clicked.original_surface) :
								component_clicked.unmask_surface()
								self.learning_cards_to_click = self.learning_cards_to_click - 1

							if (self.learning_cards_to_click <= 0) :
								self.completed = True

								self.append(self.next_icon)

								self.next_icon.draw()

								dirty1 = [self.screen.get_rect()]

	
						dirty2 = self.remove(component_clicked)
			
						sprite = ui.Sprite(component_clicked)

						self.set_dragged_sprite(sprite, (x, y))

			
						return(component_clicked, None, dirty1 + dirty2)
	
	
	
		return clicked


	def undrag_sprite(self) :

		dragged_component = self.dragged_sprite.component
				
		self.set_dragged_sprite(None)				
		
		self.append(dragged_component)

		return dragged_component.draw()



class Learning_card() :

	def __init__(self) :
		self.image_filenames = []
		self.sound_filenames = []
		self.texts = []

		self.selected = False

		self.clicked = False

	def append_image_filename(self, image_filename) :
		self.image_filenames.append(image_filename)

	def append_sound_filename(self, sound_filename) :
		self.sound_filenames.append(sound_filename)

	def append_text(self, text) :
		self.texts.append(text)

	def select_random_elements(self) :

		if (len(self.image_filenames) > 0) :
			self.image_filename = self.image_filenames[random.randint(0, len(self.image_filenames)-1)]
		else :
			self.image_filename = None

		if (len(self.texts) > 0) :
			self.text = self.texts[random.randint(0, len(self.texts)-1)]
		else :
			self.text = None


class Item_area() :

	def __init__(self, xml_node) :
	
		(self.pos, self.pos_unit, self.size, self.size_unit) = xml_funcs.get_box_with_units(xml_node)
	

	def get_pos_size(self) :
		return (self.pos, self.size)
		



class Learning_game(common.Game) :

	def __init__(self, game, main_language) :

		xml_game_node = game.xml_game_node

		self.globalvars = game.globalvars

		# here we create a new game object to play with
		# thus the original game won't be altered
		common.Game.__init__(self, self.globalvars, xml_game_node, game.level)

		self.xml_game_node = xml_game_node

		# reading global parameters
		xml_global_parameters_node = self.xml_game_node.getElementsByTagName("global_parameters")[0]
	
	
		# first of all, game setup
		xml_game_setup_node = self.xml_game_node.getElementsByTagName("game_setup")[0]
	
	
		# the min and max amounts of learning cards to display (which also happen to be draggable)
		self.min_draggable = xml_funcs.getInt(xml_game_setup_node.getElementsByTagName("min_display")[0])
		self.max_draggable = xml_funcs.getInt(xml_game_setup_node.getElementsByTagName("max_display")[0])
	

		# global placeholders where to draw learning cards

		item_area_nodes = xml_global_parameters_node.getElementsByTagName("item_to_display_area")

		self.item_areas = []
		for item_area_node in item_area_nodes :
			self.item_areas.append(Item_area(item_area_node))
		
		# area to display text legends
		text_legend_nodes = xml_global_parameters_node.getElementsByTagName("text_legend_area")

		if (len(text_legend_nodes) > 0) :
			self.text_legend_area = xml_funcs.get_box(text_legend_nodes[0])
		else :
			self.text_legend_area = None


		# reading learning_cards
		
		learning_cards_node = self.xml_game_node.getElementsByTagName("learning_cards")[0]
		
		learning_cards = learning_cards_node.getElementsByTagName("learning_card")
		
		self.learning_cards = []
		
		for learning_card_node in learning_cards :
			
			learning_card = Learning_card()
			
			image_nodes = learning_card_node.getElementsByTagName("image")
			
			for image_node in image_nodes :
				
				if (image_node.parentNode == learning_card_node) :
					# we ignore images which are not direct children
					# of the learning_card
				
					image_filename = xml_funcs.getText(image_node)
					
					learning_card.append_image_filename(image_filename)

			sound_nodes = learning_card_node.getElementsByTagName("sound")
			
			for sound_node in sound_nodes :
				sound_node_lang = sound_node.getAttribute("lang")

				if ((cmp(sound_node_lang, "") == 0) or (cmp(sound_node_lang, main_language) == 0)) :

					learning_card.append_sound_filename(xml_funcs.getText(sound_node))
					
			
			text_nodes = learning_card_node.getElementsByTagName("text")
			
			for text_node in text_nodes :

				if (text_node.parentNode == learning_card_node) :
				
					text_lang = text_node.getAttribute("lang")

					text_should_be_added = False

					if (text_lang == "") :
						# if no lang attribute defined, the text is included
						text_should_be_added = True
					else :
						# if there is a lang attribute, we add the text only
						# if this language is the main language
						if (cmp(text_lang, main_language) == 0) :
							text_should_be_added = True

						# the text node might be a dictionary key, in this case we also add it :
						if (cmp(text_node.getAttribute("key"), "") != 0) :
							text_should_be_added = True
					

					if (text_should_be_added == True) :

						text = xml_funcs.getText(text_node, self.i18n_dict, main_language)
					
						learning_card.append_text(text)
					

			self.learning_cards.append(learning_card)
			
		
		self.learning_cards = common.randomize_list(self.learning_cards)
			

	def get_random_learning_cards(self) :

		# we position images, sounds and texts which will be used
		# (in case there would be more than one in some learning_cards)		
		for learning_card in self.learning_cards :
			learning_card.select_random_elements()

		# the amount of draggable items will be a random value between min_draggable and max_draggable
		amount_draggable = self.min_draggable + random.randint(0, self.max_draggable-self.min_draggable)


		cards_amount = len(self.item_areas)
		
		self.learning_cards_to_display = []

		for i in range(cards_amount) :
		
			for learning_card in self.learning_cards :
				if (learning_card.selected == False) :
					if (learning_card not in self.learning_cards_to_display) :
						self.learning_cards_to_display.append(learning_card)

						break
			else :
				# if all the learning_cards were found, there's nothing more to draw !
				raise common.EndActivityException()
	
		
		return

def next_page(game, globalvars) :

	game.get_random_learning_cards()

	game.rounds_done = game.rounds_done + 1

	if (game.rounds_done < game.rounds_amount + 1) :

		current_page = Page_learning(game, globalvars)

		current_page.fade_in()
		pygame.display.flip()
		
		if (cmp(game.music_mode, "off") == 0) :
			# if silence was requested (no music)
			# we make sure no more sound will be heard from previous page
			pygame.mixer.fadeout(constants.fadeout_sound_duration)

		return current_page
	
	else :
		common.info("No more learning_cards to look for !")
	
		return None



class Run_Learning_Screen(common.Run_Screen) :

	def __init__(self, game, globalvars) :

		common.info("Running learning game")
		
		game = Learning_game(game, globalvars.main_language)

		common.Run_Screen.__init__(self, globalvars, game)		

		self.current_page = next_page(self.game, self.globalvars)

		while self.running :

			common.Run_Screen.run_pre(self)
	
			# actions after keyboard events	

			goto_next_page = False

			for key_event in self.key_events :

				if (key_event.key == K_SPACE) :
					if (self.current_page.completed == True) :
						goto_next_page = True


			if (self.mouse_clicked == True) :
			
				clicked = self.current_page.was_something_clicked(self.mouse_pos, self.mousebutton)
					
				if (clicked != None) :
					(component_clicked, foo, some_dirty_rects) = clicked
		
					# we try to play an associated sound (if any)
					component_clicked.play_random_associated_sound()
		
					if (component_clicked == self.current_page.quit_icon) :
						raise common.EndActivityException()

					elif (component_clicked == self.current_page.next_icon) :

						goto_next_page = True



					self.dirty_rects = self.dirty_rects + some_dirty_rects
						

			# mouse may be going over elements

			if (self.current_page.dragged_sprite == None) :
				
				# yet mouse over is checked only when no object is being dragged

				(mouse_over_new, mouse_over_old) = self.current_page.components_mouse_over(pygame.mouse.get_pos())

				if (mouse_over_old != None) :
					self.dirty_rects = self.dirty_rects + self.current_page.remove_legend_text()

				if (mouse_over_new != None) :
					self.dirty_rects = self.dirty_rects + self.current_page.add_legend_text(mouse_over_new)


			if (goto_next_page == True) :
				self.current_page.fade_out()

				self.current_page = next_page(self.game, globalvars)

				if (self.current_page == None) :
					return


			common.Run_Screen.run_post(self)	
