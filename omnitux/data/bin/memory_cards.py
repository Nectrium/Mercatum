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

import pygame, random, copy
from pygame.locals import *
			
import ui, constants, xml_funcs, i18n, common

class Page_memory_cards(ui.Game_Page) :


	def __init__(self, game, globalvars, associations) :
		
		
		self.associations = associations

		# completed becomes True when all cards have disappeared
		self.completed = False
		
		ui.Game_Page.__init__(self, globalvars, game)

	
	def update(self) :
		
		ui.Page.update(self)
		

		((grid_x,grid_y), (grid_width, grid_height)) = self.game.grid_box

		width_card = (grid_width - ((self.game.grid_amount_x - 1.0) * self.game.spacing_x)) / self.game.grid_amount_x
		height_card = (grid_height - ((self.game.grid_amount_y - 1.0) * self.game.spacing_y)) / self.game.grid_amount_y

		self.back_cards_images = []

		# draw the back of the cards, and prepare the front
		for x_index in range(self.game.grid_amount_x) :
			for y_index in range(self.game.grid_amount_y) :

				x = grid_x + (x_index * (width_card + self.game.spacing_x))
				y = grid_y + (y_index * (height_card + self.game.spacing_y))

				# the back 

				back_card_image = ui.Image(self, (x, y), (width_card, height_card), self.game.back_card_file)

				self.append(back_card_image)
				self.back_cards_images.append(back_card_image)
		
				# the front

				# conversion of box coordinates to fit inside the back of the cards
				# which were created above
				x_front = self.x_px2pc(back_card_image.rect.left)
				y_front = self.y_px2pc(back_card_image.rect.top)

				width_card_front = self.x_px2pc(back_card_image.rect.width)
				height_card_front = self.y_px2pc(back_card_image.rect.height)


				association = self.associations[random.randint(0, len(self.associations) - 1)]
				
				while (association.counter >= self.game.amount_identical_cards) :
					association = self.associations[random.randint(0, len(self.associations) - 1)]

				association.counter = association.counter + 1


				front_card_empty_image = ui.Image(self, (x_front, y_front), (width_card_front, height_card_front), self.game.front_card_file)


				width_card_front_image = width_card_front * (self.game.ratio_x / 100.0)
				height_card_front_image = height_card_front * (self.game.ratio_y / 100.0)

				x_front_image = x_front + ((width_card_front - width_card_front_image) / 2.0)
				y_front_image = y_front + ((height_card_front - height_card_front_image) / 2.0)

				front_card_image = ui.Image(self, (x_front_image, y_front_image), (width_card_front_image, height_card_front_image), association.selected_image)


				# TODO : put the sound on the back of the card
				if (association.selected_image in association.image_sounds) :
					back_card_image.associated_sounds = association.image_sounds[association.selected_image]
					front_card_image.associated_sounds = association.image_sounds[association.selected_image]

				# the associated objects allow to link between the back card until the image component and then the association

				back_card_image.set_associated_object(front_card_empty_image)
				front_card_empty_image.set_associated_object(front_card_image)
				front_card_image.set_associated_object(association)


		self.selected_back_cards = []

		self.draw_back()


	def was_something_clicked(self, (x, y), mousebutton) :
	
		clicked = ui.Page.was_something_clicked(self, (x,y), mousebutton)		
		
		if (clicked != None) :
			(component_clicked, foo, some_dirty_rects) = clicked

			# we try to play an associated sound (if any)
			component_clicked.play_random_associated_sound()

			if ((component_clicked in self.back_cards_images) and (component_clicked not in self.selected_back_cards)) :

				dirty_rects = []

				if (len(self.selected_back_cards) >= self.game.amount_identical_cards) :
					# hide the front of the cards
					for selected_back_card in self.selected_back_cards :

						front_card_empty_image = selected_back_card.associated_object
						front_card_image = front_card_empty_image.associated_object
	
						self.remove(front_card_empty_image)
						self.remove(front_card_image)

						dirty_rects = dirty_rects + [front_card_empty_image.rect, front_card_image.rect]

					self.selected_back_cards = []



				# "turn" a card to show its front
				front_card_empty_image = component_clicked.associated_object
				front_card_image = front_card_empty_image.associated_object

				self.append(front_card_empty_image)
				self.append(front_card_image)

				front_card_empty_image.draw()
				front_card_image.draw()

				self.selected_back_cards.append(component_clicked)

				dirty_rects = dirty_rects +  [front_card_empty_image.rect, front_card_image.rect]


				# did the player select identical cards ?
				if (len(self.selected_back_cards) == self.game.amount_identical_cards) :
					all_identical = True

					front_card_empty_image = self.selected_back_cards[0].associated_object
					front_card_image = front_card_empty_image.associated_object
					association = front_card_image.associated_object

					for selected_back_card in self.selected_back_cards :
						front_card_empty_image = selected_back_card.associated_object
						front_card_image = front_card_empty_image.associated_object
						new_association = front_card_image.associated_object
						
						if (new_association != association) :
							all_identical = False
					
					if (all_identical == True) :
						
						common.info("Good answer")

						pygame.display.update(dirty_rects)
						



						# completely hide the cards
						for selected_back_card in self.selected_back_cards :

							self.back_cards_images.remove(selected_back_card)

							front_card_empty_image = selected_back_card.associated_object
							front_card_image = front_card_empty_image.associated_object
							
							self.remove(selected_back_card)
							self.remove(front_card_empty_image)
							self.remove(front_card_image)

							dirty_rects = dirty_rects + [front_card_empty_image.rect, front_card_image.rect, selected_back_card.rect]

						self.selected_back_cards = []

						pygame.time.wait(constants.memory_wait_time)
						
						if (len(self.back_cards_images) == 0) : 
							# all the cards were found

							self.game.stop_timer()

							common.info("All the cards were found")

							self.append(self.next_icon)

							dirty_rects = dirty_rects + self.next_icon.draw()
						

							self.play_congratulations_sound()


				return (component_clicked, foo, some_dirty_rects + dirty_rects)
	
		return clicked

class Association() :
	def __init__(self, game) :
		self.game = game

		# filename(s) of image(s)
		self.images = []
		self.image_sounds = {}
		
		self.selected = False

		# this counter will grow until the image is associated with as many cards as needed
		# (generally two)
		self.counter = 0
		
	def append_image_sound(self, image_file, sound) :
		if (image_file not in self.image_sounds) :
			self.image_sounds[image_file] = [sound]
		else :
			self.image_sounds[image_file].append(sound)


	def select_random_image(self) :
		# select a random image to memorize
		self.selected_image = self.images[random.randint(0, len(self.images)-1)]
	


class Memory_cards_game(common.Game) :

	def __init__(self, game, score) :
		
		self.globalvars = game.globalvars

		# creation of a new game
		common.Game.__init__(self, self.globalvars, game.xml_game_node, game.level, score)

		self.score.enable_record_time()


		if (self.xml_game_node != None) :

			# reading global parameters
			xml_global_parameters_node = self.xml_game_node.getElementsByTagName("global_parameters")[0]
		

			# the amount of identical cards to find
			self.amount_identical_cards = xml_funcs.getInt(xml_global_parameters_node.getElementsByTagName("identical_cards")[0])


			# Grid setup
			grid_node  = xml_global_parameters_node.getElementsByTagName("grid")[0]
			
			self.grid_box = xml_funcs.get_box(grid_node)
			
			self.grid_amount_x = xml_funcs.getInt(grid_node.getElementsByTagName("amount_x")[0])
			self.grid_amount_y = xml_funcs.getInt(grid_node.getElementsByTagName("amount_y")[0])


			self.amount_different_cards = int((1.0 * self.grid_amount_x * self.grid_amount_y) / self.amount_identical_cards)

			if (self.amount_different_cards != round(self.amount_different_cards)) :
				common.error("the amount of cards is not a multiple of the amount of cards to group")
				raise common.BadXMLException()


			spacing_x_nodes = grid_node.getElementsByTagName("spacing_x")
			spacing_y_nodes = grid_node.getElementsByTagName("spacing_y")

			if (len(spacing_x_nodes) > 0) :
				self.spacing_x = xml_funcs.getFloat(spacing_x_nodes[0])
			else :
				self.spacing_x = 0

			if (len(spacing_y_nodes) > 0) :
				self.spacing_y = xml_funcs.getFloat(spacing_y_nodes[0])
			else :
				self.spacing_y = 0

			# card setup
			card_node  = xml_global_parameters_node.getElementsByTagName("card")[0]

			front_card_node = card_node.getElementsByTagName("front")[0]
			self.front_card_file = xml_funcs.getText(front_card_node)

			back_card_node = card_node.getElementsByTagName("back")[0]
			self.back_card_file = xml_funcs.getText(back_card_node)

			image_area_nodes = xml_global_parameters_node.getElementsByTagName("image_area")
			if (len(image_area_nodes) > 0) :
				image_area_node = image_area_nodes[0]

				ratio_x_node = image_area_node.getElementsByTagName("ratio_x")[0]
				self.ratio_x = xml_funcs.getFloat(ratio_x_node)

				ratio_y_node = image_area_node.getElementsByTagName("ratio_y")[0]
				self.ratio_y = xml_funcs.getFloat(ratio_y_node)
			else :
				self.ratio_x = 100.0
				self.ratio_y = 100.0


			# reading associations
			# (here, only images with associated sounds are supported)
			
			associations_node = self.xml_game_node.getElementsByTagName("associations")[0]
			
			associations = associations_node.getElementsByTagName("association")
			
			self.associations = []
			
			for association_node in associations :
				
				association = Association(self)
				
				image_nodes = association_node.getElementsByTagName("image")
				
		
				for image_node in image_nodes :
						
					image_filename = xml_funcs.getText(image_node)
					
					association.images.append(image_filename)
							

					sound_nodes = image_node.getElementsByTagName("sound")
					
					for sound_node in sound_nodes :
						association.append_image_sound(image_filename, xml_funcs.getText(sound_node))
						

				
				self.associations.append(association)

			if (len(self.associations) < self.amount_different_cards) :
				common.error("The XML file contains " + str(len(self.associations)) + " associations")
				common.error("But at least "+str(self.amount_different_cards) + " associations are required")
				raise common.BadXMLException()

		
			self.associations = common.randomize_list(self.associations)
				

	def get_random_associations(self) :

		random_associations = []
		
		for i in range(self.amount_different_cards) :

			for association in self.associations :
				if (association.selected == False) :
			
					association.selected = True

					random_associations.append(association)

					break
			else :
				# if all the associations were selected and we still need one, there's a setup problem !
				
				common.error("Not enough associations available. Please check your XML setup.")
				
				return (None, None)

		# we position images and texts which might be displayed
		# (in case there would be more than one in some associations)		
		for association in random_associations :
			association.select_random_image()

		return random_associations


class Run_Memory_Cards_Screen(common.Run_Screen) :

	def __init__(self, game, globalvars, total_score) :

		common.info("Running memory cards activity")

		game = Memory_cards_game(game, total_score)
		
		random_associations = game.get_random_associations()
		
		common.Run_Screen.__init__(self, globalvars, game)

		self.current_page = Page_memory_cards(self.game, globalvars, random_associations)
		
		self.current_page.draw()
		pygame.display.flip()

		game.start_timer()

		while self.running :

			common.Run_Screen.run_pre(self)

			# actions after keyboard events	

			for key_event in self.key_events :
				if key_event.key == K_SPACE :
					if (self.current_page.completed == True) :
						return
					
		
			if (self.mouse_clicked == True) :
			
				clicked = self.current_page.was_something_clicked(self.mouse_pos, self.mousebutton)
					
				if (clicked != None) :
					(component_clicked, foo, some_dirty_rects) = clicked
		
					if (component_clicked == self.current_page.quit_icon) :
						raise common.EndActivityException()

					elif (component_clicked == self.current_page.next_icon) :
						return

					self.dirty_rects = self.dirty_rects + some_dirty_rects

				
			common.Run_Screen.run_post(self)	

			
