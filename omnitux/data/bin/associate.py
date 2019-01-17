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
			
import ui, constants, xml_funcs, i18n, common, display_big


class Page_associate(ui.Game_Page) :

	# the idea is to find 1 to n associations, 
	# - those associations are stored into the good_associations list
	# - the all_associations list contains the "good associations", plus some more
	# which "do not match" (except if their associations happen to be "equivalent")
	#
	# items_to_associate : items displayed (images, texts). The player has to associate another item to them
	# goals : the places where items have to be dragged and dropped to find the association (textboxes, images)
	# draggable_items : items which can be dragged and dropped to make an association 

	def __init__(self, game, globalvars, good_associations, all_associations) :

		self.dragged_sprite = None
		
		self.good_associations = good_associations
		self.all_associations = all_associations
		
		self.items_to_associate = []
		
		self.draggable_items = []

		#self.text_height = self.game.text_height

		self.goals = []

		# completed becomes True when all associations have been done in the page
		self.completed = False
		
		ui.Game_Page.__init__(self, globalvars, game)
		
	
	def update(self) :
		
		ui.Page.update(self)


		if (cmp(self.game.type_to_associate, "image_on_map") == 0) :
			self.map_image = ui.Image(self, self.game.map_pos, self.game.map_size, self.game.map_filename)
			
			self.append_back(self.map_image)
			
		else :
			self.map_image = None


		# adding the items to associate and the placeholders for answers (goals)
		self.goals_to_find = 0
		
		for good_association in self.good_associations :	

			if (good_association.selected_item_to_associate != None) :
				# get a random graphical representation (image or text) for the "good" associations	
				item_to_associate = good_association.create_graphical_representation(self, self.goals_to_find, self.map_image)
				
				self.items_to_associate.append(item_to_associate)		
				self.append(item_to_associate)


			# The goals are the places where to drag and drop the text or image
			# there should be one goal for each good association
			
			goal = good_association.create_graphical_goal(self, self.goals_to_find, self.map_image)
			
			self.goals.append(goal)
			self.append(goal)
	

			self.goals_to_find = self.goals_to_find + 1	


		# adding the "draggable" items

		self.index_draggable_item = 0
		self.index_draggable_area = 0

		for association in (self.all_associations) :
			
			draggable_item = association.create_draggable_item(self)

			self.append(draggable_item)
			self.draggable_items.append(draggable_item)


		# eventually adding text legend
		if (self.game.text_legend_area != None) :
			(self.legend_text_pos, self.legend_text_size) = self.game.text_legend_area


		self.draw_back()


	def was_something_clicked(self, (x, y), mousebutton) :
	
		clicked = ui.Page.was_something_clicked(self, (x,y), mousebutton)		
	
		if (clicked != None) :
			(component_clicked, foo, dirty1) = clicked	
			
			if ((self.dragged_sprite == None) and (mousebutton == 1)) :
				# this might be an item to drag 
				
				for draggable_item in self.draggable_items :
					
					if (component_clicked == draggable_item) :
	
						dirty2 = self.remove(component_clicked)
			
						sprite = ui.Sprite(component_clicked)

						self.set_dragged_sprite(sprite, (x, y))
			
						return(component_clicked, None, dirty1 + dirty2)
	
	
	
		return clicked


	def undrag_sprite(self) :

		dragged_component = self.dragged_sprite.component
				
			
		goal_found = False
		
		dropped_on_goal_area = False
		
		for goal in self.goals :
			
			dragged_component_modified_rect = Rect((0,0), (min(goal.rect.width, dragged_component.rect.width), min(goal.rect.height, dragged_component.rect.height)))
			dragged_component_modified_rect.center = dragged_component.rect.center

			if (dragged_component_modified_rect.colliderect(goal)) :
				
				dropped_on_goal_area = True
				
				# let's check whether the dragged component is the one associated with the goal
				# OR whether it is another association, which happens to be equivalent (has text
				# in common, and sound in common if present)
				if ((dragged_component.associated_object == goal.associated_object) or 
					(dragged_component.associated_object.is_equivalent(goal.associated_object))) :
					
					# that is a good answer !
					
					goal_found = True
					
					common.info("Good answer")
					
					self.play_congratulations_sound()
					
					self.game.score.good_answer()

					if (cmp(self.game.type_to_drag, "text") == 0) :
						goal.set_text(dragged_component.get_text())
						
						new_goal = goal
					else :
						goal_rect = goal.get_original_rect()
						new_goal = ui.Image(self, (self.x_px2pc(goal_rect.left), self.y_px2pc(goal_rect.top)), (self.x_px2pc(goal_rect.width), self.y_px2pc(goal_rect.height)), dragged_component.associated_object.selected_item_to_drag)
						
						new_goal.associated_object = dragged_component.associated_object

						self.remove(goal)
												
						self.append(new_goal)
					
					self.goals.remove(goal)
					
					
					new_goal.associated_sounds = dragged_component.associated_sounds
					new_goal.associated_text = dragged_component.associated_text
					new_goal.associated_text_color = dragged_component.associated_text_color
						
					if (new_goal.associated_text != None) :
						self.listen_to_mouse_over(new_goal)

			
					# this image / text association is now done
					new_goal.associated_object.done = True
					
					self.draggable_items.remove(dragged_component)

					
					self.goals_to_find = self.goals_to_find - 1
					
					if (self.goals_to_find == 0) :
					
						# removal of all the mobile stuff
						
						for draggable_item in self.draggable_items :
							self.remove(draggable_item)
					
						# this game page is now complete
						self.completed = True
					
					break

		if (goal_found == False) :
			# bad answer
			# so we go back to initial place
			dragged_component.rect = self.dragged_sprite.initial_pos
			
			if (cmp(self.game.type_to_drag, "text") == 0) :
			
				# useful only for textboxes
			
				dragged_component.text_component.rect = self.dragged_sprite.initial_pos
				dragged_component.box_component.rect = self.dragged_sprite.initial_pos		
			
			if (dropped_on_goal_area == True) :
				# sound is played only in case of mistake

				self.game.score.wrong_answer()

				self.play_error_sound()

		self.set_dragged_sprite(None)				
		
		if (goal_found == False) :
			self.append(dragged_component)

			if (dragged_component.associated_text != None) :
				self.listen_to_mouse_over(dragged_component)
		
			return dragged_component.draw()

		else :
			dirty_rects = goal.erase() + new_goal.draw() 

			if (self.completed == True) :

				self.game.stop_timer()

				self.append(self.next_icon)

				self.next_icon.draw()

				dirty_rects = [self.screen.get_rect()]

			return dirty_rects


class Association() :
	def __init__(self, game) :
		self.game = game

		# TODO images => images_to_associate
		
		# images_to_associate : a list of images to associate to others (ie: the drag and dropped ones)
		# images to drag : a list of images which can be dragged and dropped
		
		# image_sounds : a dictionary of sounds associated with each image (can be empty !)
		# used for both image types (to associate or to drag)
		# image_text_legends : same idea as image_sounds but with text legends (single language at this point)
		self.images_to_associate = []
		self.images_to_drag = []
		self.image_sounds = {}
		self.image_text_legends = {}


		# texts : a list of associated text(s)
		# text_sounds : a dictionary of sounds associated with each text (can be empty !)			
		self.texts = []
		self.text_sounds = {}
		
		self.done = False
		
	def append_image_sound(self, image_file, sound) :
		if (image_file not in self.image_sounds) :
			self.image_sounds[image_file] = [sound]
		else :
			self.image_sounds[image_file].append(sound)

	def append_image_text_legend(self, image_file, text_legend) :
		if (image_file not in self.image_text_legends) :
			self.image_text_legends[image_file] = [text_legend]
		else :
			self.image_text_legends[image_file].append(text_legend)
		
	def append_text_sound(self, text, sound) :
		if (text not in self.text_sounds) :
			self.text_sounds[text] = [sound]
		else :
			self.text_sounds[text].append(sound)


	def select_random_items(self) :
		# select a random item to associate
		# and a random item to drag and drop
		if (cmp(self.game.type_to_associate, "image") == 0)  :
			self.selected_item_to_associate = self.images_to_associate[random.randint(0, len(self.images_to_associate)-1)]
		elif (cmp(self.game.type_to_associate, "image_on_map") == 0) :
			if (len(self.images_to_associate) > 0) :
				self.selected_item_to_associate = self.images_to_associate[random.randint(0, len(self.images_to_associate)-1)]
			else :
				self.selected_item_to_associate = None
		

		if (cmp(self.game.type_to_drag, "image") == 0) :
			self.selected_item_to_drag = self.images_to_drag[random.randint(0, len(self.images_to_drag)-1)]
		elif (cmp(self.game.type_to_drag, "text") == 0) :
			self.selected_item_to_drag = self.texts[random.randint(0, len(self.texts)-1)]


	# TODO: make another function different of cmp !

	#def __cmp__(self, other) :
		## used to order the texts by alphabetical order
		#return cmp(self.selected_item_to_drag, other.selected_item_to_drag)


	def is_equivalent(self, other_association) :
		# compares two associations
		# if items dragged are text :
			# returns true if their texts and sounds are "equivalent", ie identical
		# if items dragged are images :
			# returns true if the images and their sounds are identical
		
		if (cmp(self.game.type_to_drag, "text") == 0) :
			# compares text elements
			for text in self.texts :
				if (text not in other_association.texts) :
					return False
				
			for text_sound in self.text_sounds :
				if (text_sound not in other_association.text_sounds) :
					return False

			return True
			
		else :
			# compares image elements
			for image in self.images_to_drag :
				if (image not in other_association.images_to_drag) :
					return False

				for image_sound in self.image_sounds[image] :
					if (image_sound not in other_association.image_sounds[image]) :
						return False

			return True
		

	def create_graphical_representation(self, page, index_goal, map_image) :
		
		
		if (cmp(self.game.type_to_associate, "image_on_map") <> 0) :
			(image_pos, image_size) = self.game.item_to_associate_parameters[index_goal]
		else :
			(image_pos, image_size) = self.image_to_associate_pos_size
		
			coords_converter = ui.Coordinates_converter(page, Rect((0,0), map_image.original_size), map_image.rect)
		
			image_pos = coords_converter.get_coords_pc_org2pc(image_pos)
			image_size = coords_converter.get_size_pc_org2pc(image_size)
		
		
		image = ui.Image(page, image_pos, image_size, self.selected_item_to_associate)
	
		image.set_associated_object(self)
	
		if (self.selected_item_to_associate in self.image_sounds) :
			image.associated_sounds = self.image_sounds[self.selected_item_to_associate]

		if (self.selected_item_to_associate in self.image_text_legends) :
			# MAYBETODO : allow various text legends ?
			image.set_associated_text(self.image_text_legends[self.selected_item_to_associate][0])

			page.listen_to_mouse_over(image)
			
		return image
		
	def create_graphical_goal(self, page, index_goal, map_image) :
			
		if (cmp(self.game.type_to_associate, "image_on_map") <> 0) :
			goal = self.game.goals[index_goal]
			
			if (goal.text != None) :
				goal = ui.TextBox(page, goal.text, goal.pos, goal.size, page.fonts, constants.text_color, 1)
			else :
				goal = ui.Image(page, goal.pos, goal.size, goal.image_file)

			if (self.selected_item_to_associate in self.image_sounds) :
				goal.associated_sounds = self.image_sounds[self.selected_item_to_associate]

			
		else :
			goal = self.associated_goal
			
			goal.place_on_map(map_image)
			
			# TODO : implement textbox
			# goal = ui.TextBox(page, goal.text, goal.pos, goal.size, page.fonts, constants.text_color, 1, goal.image_file, 0)
			
			goal = ui.Image(page, goal.pos, goal.size, goal.image_file)
				
		goal.set_associated_object(self)
		
		return goal
	
	def create_draggable_item(self, page) :
		
		# items are organized left to right
		# they go down after the right limit is reached
		
		((draggable_area_pos, draggable_area_size), amount_x, amount_y, spacing_x, spacing_y) = self.game.draggable_items_areas[page.index_draggable_area]	

		step_x = draggable_area_size[0] / amount_x
		step_y = draggable_area_size[1] / amount_y
		
		x_pos = page.index_draggable_item % amount_x
		y_pos = page.index_draggable_item // amount_x
		
		offset_x = (step_x * x_pos) + spacing_x
		offset_y = (step_y * y_pos) + spacing_y

		page.index_draggable_item = page.index_draggable_item + 1
		if (page.index_draggable_item >= amount_x * amount_y) :
			page.index_draggable_item = 0
			page.index_draggable_area = page.index_draggable_area + 1

		
		if (cmp(self.game.type_to_drag, "text") == 0) :

			# TODO implement spacing here

			textbox = ui.TextBox(page, self.selected_item_to_drag, (draggable_area_pos[0] + offset_x, draggable_area_pos[1] + offset_y), (draggable_area_size[0] // amount_x, self.game.text_height), page.fonts, constants.text_color, 11)

			textbox.set_associated_object(self)
	
			if (self.selected_item_to_drag in self.text_sounds) :
				textbox.associated_sounds = self.text_sounds[self.selected_item_to_drag]
				
			return textbox
	
		elif (cmp(self.game.type_to_drag, "image") == 0) :
			
			image_file = self.selected_item_to_drag
			
			(image_pos, image_size) = (	(draggable_area_pos[0] + offset_x, 
							draggable_area_pos[1] + offset_y), 
							((draggable_area_size[0] // amount_x) - (2 * spacing_x), 
							(draggable_area_size[1] // amount_y) - (2 * spacing_y)  ) )
			
			image = ui.Image(page, image_pos, image_size, image_file)
		
			image.set_associated_object(self)
		
			if (image_file in self.image_sounds) :
				image.associated_sounds = self.image_sounds[image_file]

			if (image_file in self.image_text_legends) :
				# MAYBETODO : allow various text legends ?
				image.set_associated_text(self.image_text_legends[image_file][0])

				page.listen_to_mouse_over(image)
			
			return image
			
		else :
			error("Incorrect value for type_to_drag"+self.game.type_to_drag)
			error("Correct values are: text, image")
	
			return None

	def get_infos_for_display_big_to_drag(self) :
		if (cmp(self.game.type_to_drag, "image") == 0) :
			return(None, self.selected_item_to_drag, None)
		else :
			return(None, None, None)

	def get_infos_for_display_big_to_associate(self) :
		if ((cmp(self.game.type_to_associate, "image") == 0) or (cmp(self.game.type_to_associate, "image_on_map") == 0)) :
			return(None, self.selected_item_to_associate, None)
		else :
			return(None, None, None)



class Goal() :

	def __init__(self, xml_node) :
		#Transforms xml goal into a goal object
	
		(self.pos, self.pos_unit, self.size, self.size_unit) = xml_funcs.get_box_with_units(xml_node)
	
		image_file_nodes = xml_node.getElementsByTagName("image")
		
		if (len(image_file_nodes) > 0) :
			self.image_file = xml_funcs.getText(image_file_nodes[0])
		else :
			self.image_file = None
		
		if (self.image_file == None) :
			# TODO: to add from XML
			self.text = "?"
		else :
			self.text = None

	def get_pos_size(self) :
		return (self.pos, self.size)
		
	def place_on_map(self, map_image) :

		coords_converter = ui.Coordinates_converter(map_image.page, Rect((0,0), map_image.original_size), map_image.rect)

		self.size = coords_converter.get_size_pc_org2pc(self.size)
		
		if (cmp(self.pos_unit, "pc") == 0) :

			self.pos = coords_converter.get_coords_pc_org2pc(self.pos)

		else :
			(x_percent, y_percent) = coords_converter.get_coords_px2pc(self.pos)

			(width, height) = self.size

			self.pos = (x_percent - (width / 2), y_percent - (height / 2))



class Associate_game(common.Game) :

	def __init__(self, game, main_language, score) :

		xml_game_node = game.xml_game_node

		self.globalvars = game.globalvars

		# here we create a new game object to play with
		# thus the original game won't be altered

		common.Game.__init__(self, self.globalvars, xml_game_node, game.level, score)

		self.score.enable_count_good()
		self.score.enable_count_wrong()
		self.score.enable_record_time()


		self.xml_game_node = xml_game_node

		# reading global parameters
		xml_global_parameters_node = self.xml_game_node.getElementsByTagName("global_parameters")[0]
	
	
		# first of all, game setup
		xml_game_setup_node = self.xml_game_node.getElementsByTagName("game_setup")[0]
	
		# possible values for types :
		# image
		# image_on_map (only to associate)
		# text
		self.type_to_associate = xml_funcs.getText(xml_game_setup_node.getElementsByTagName("type_to_associate")[0])
		
		type_to_drag_node = xml_game_setup_node.getElementsByTagName("type_to_drag")[0]

		self.type_to_drag = xml_funcs.getText(type_to_drag_node)
		sort = type_to_drag_node.getAttribute("sort")
		
		if (sort == None) :
			self.sort = False
		elif (cmp(sort.lower(), "yes") == 0) :
			self.sort = True
		else :
			self.sort = False
		
		
	
		# the min and max amounts of associations (good + bad ones) which will become draggable items
		self.min_draggable = xml_funcs.getInt(xml_game_setup_node.getElementsByTagName("min_draggable")[0])
		self.max_draggable = xml_funcs.getInt(xml_game_setup_node.getElementsByTagName("max_draggable")[0])
	
	
		item_to_associate_parameters_nodes  = xml_global_parameters_node.getElementsByTagName("item_to_associate")
		
		self.item_to_associate_parameters = []
		for item_to_associate_parameters_node in item_to_associate_parameters_nodes :
			self.item_to_associate_parameters.append(xml_funcs.get_box(item_to_associate_parameters_node))


		draggable_items_area_nodes = xml_global_parameters_node.getElementsByTagName("draggable_items_area")
		self.draggable_items_areas = []
		
		for draggable_items_area_node in draggable_items_area_nodes :

			spacing_x_nodes = draggable_items_area_node.getElementsByTagName("spacing_x")
			spacing_y_nodes = draggable_items_area_node.getElementsByTagName("spacing_y")

			if (len(spacing_x_nodes) > 0) :
				spacing_x = xml_funcs.getFloat(spacing_x_nodes[0])
			else :
				spacing_x = 0

			if (len(spacing_y_nodes) > 0) :
				spacing_y = xml_funcs.getFloat(spacing_y_nodes[0])
			else :
				spacing_y = 0

			draggable_items_area = (xml_funcs.get_box(draggable_items_area_node),
						xml_funcs.getInt(draggable_items_area_node.getElementsByTagName("amount_x")[0]),
						xml_funcs.getInt(draggable_items_area_node.getElementsByTagName("amount_y")[0]),
						spacing_x,
						spacing_y)
			
			# TODO: make this under each area
			
			text_height_nodes = draggable_items_area_node.getElementsByTagName("font_height")
			if (len(text_height_nodes) > 0) :
				self.text_height = xml_funcs.getInt(text_height_nodes[0])
			else :
				self.text_height = None
			
			self.draggable_items_areas.append(draggable_items_area)
		

		# global placeholders where to drag items
		# only present for non-map associations
		goal_nodes = xml_global_parameters_node.getElementsByTagName("goal")

		self.goals = []
		for goal_node in goal_nodes :
		
			goal = Goal(goal_node)
		
			self.goals.append(goal)
		

		# space to display text legends
		text_legend_nodes = xml_global_parameters_node.getElementsByTagName("text_legend_area")

		if (len(text_legend_nodes) > 0) :
			self.text_legend_area = xml_funcs.get_box(text_legend_nodes[0])
		else :
			self.text_legend_area = None



		
		# Map information (only present if type_to_associate is "on_map")
		map_nodes = xml_global_parameters_node.getElementsByTagName("map")

		if (len(map_nodes) > 0) :
			map_node = map_nodes[0]
			
			(self.map_pos, self.map_size) = xml_funcs.get_box(map_node)
			
			map_filenames = map_node.getElementsByTagName("image")
			
			self.map_filename = xml_funcs.getText(map_filenames[0])



		# reading associations
		
		associations_node = self.xml_game_node.getElementsByTagName("associations")[0]
		
		associations = associations_node.getElementsByTagName("association")
		
		self.associations = []
		
		for association_node in associations :
			
			association = Association(self)
			
			image_nodes = association_node.getElementsByTagName("image")
			
	
			for image_node in image_nodes :
				
				if (image_node.parentNode == association_node) :
					# we ignore images which are not direct children
					# of the association (ie: images inside goal for instance)
				
					image_filename = xml_funcs.getText(image_node)
					

					if (cmp(image_node.getAttribute("type"), "") == 0) :
						if (cmp(self.type_to_associate, "image") == 0) :
							association.images_to_associate.append(image_filename)
						if (cmp(self.type_to_drag, "image") == 0) :
							association.images_to_drag.append(image_filename)
							
					elif (cmp(image_node.getAttribute("type"), "to_associate") == 0) :
						if ((cmp(self.type_to_associate, "image") == 0) or (cmp(self.type_to_associate, "image_on_map") == 0)) :
							association.images_to_associate.append(image_filename)
	
							if (cmp(self.type_to_associate, "image_on_map") == 0) :
								association.image_to_associate_pos_size = xml_funcs.get_box(image_node)
	
						else :
							common.warn(image_filename + " is supposed to be associated, but the game is not supposed to associate images")
							
					elif (cmp(image_node.getAttribute("type"), "to_drag") == 0) :
						if ((cmp(self.type_to_drag, "image") == 0) or (cmp(self.type_to_associate, "image_on_map") == 0)) :
							association.images_to_drag.append(image_filename)
						else :
							common.warn(image_filename + " is supposed to be dragged and dropped, but the game is not supposed to drag an drop images")
						
					# find potential associated sounds

					sound_nodes = image_node.getElementsByTagName("sound")
					
					for sound_node in sound_nodes :
						sound_node_lang = sound_node.getAttribute("lang")

						if ((cmp(sound_node_lang, "") == 0) or (cmp(sound_node_lang, main_language) == 0)) :

							association.append_image_sound(image_filename, xml_funcs.getText(sound_node))

					# find potential associated text legends
					# only texts with no lang tag or with lang tag = main_language are used
					text_legend_nodes = image_node.getElementsByTagName("text")
					
					for text_legend_node in text_legend_nodes :

						if ((cmp(text_legend_node.getAttribute("lang"), main_language) == 0) or (cmp(text_legend_node.getAttribute("key"), "") != 0)) :

							association.append_image_text_legend(image_filename, xml_funcs.getText(text_legend_node, self.i18n_dict, main_language))					

					
			
			text_nodes = association_node.getElementsByTagName("text")
			
			for text_node in text_nodes :

				if (text_node.parentNode == association_node) :
				
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
					
						association.texts.append(text)
					
						sound_nodes = text_node.getElementsByTagName("sound")
					
						for sound_node in sound_nodes :

							sound_node_lang = sound_node.getAttribute("lang")

							if ((cmp(sound_node_lang, "") == 0) or (cmp(sound_node_lang, main_language) == 0)) :
	
								association.append_text_sound(text, xml_funcs.getText(sound_node))
				
				
			# goals local to only one association
			
			goal_nodes = association_node.getElementsByTagName("goal")
			
			if (len(goal_nodes) > 0) :
			
				# TODO : allow for more than a goal ?
				goal_node = goal_nodes[0]
				
				if (cmp(self.type_to_associate, "image_on_map") == 0) :
					
					goal = Goal(goal_node)

					# TODO : remove from here ?				
					self.goals.append(goal)
					
					# TODO : put more than one goal
					association.associated_goal = goal
			
				else :
					common.warn("<goal> found inside an association whereas type to associate is not image_on_map")
			
			
			
			
			self.associations.append(association)
			
		
		self.associations = common.randomize_list(self.associations)
			

	def get_random_associations(self) :

		# we position images and texts which might be displayed
		# (in case there would be more than one in some associations)		
		for association in self.associations :
			association.select_random_items()

		# the amount of draggable items will be a random value between min_draggable and max_draggable
		if (self.score.get_arcade_mode() == False) :
			amount_draggable = self.min_draggable + random.randint(0, self.max_draggable-self.min_draggable)
		else :
			# in arcade mode, we force the maximum amount of drag objects
			amount_draggable = self.max_draggable


		# taking a random association
		# those will be the "good" answers
		good_associations = []
		
		if (cmp(self.type_to_associate, "image_on_map") == 0):
			goals_to_find = amount_draggable

		else :
			goals_to_find = len(self.goals)
		

		for i in range(goals_to_find) :
		
			for association in self.associations :
				if (association.done == False) :
					if (association not in good_associations) :
						good_associations.append(association)

						break
			else :
				# if all the associations were found, there's nothing more to associate !
				
				common.info("Not enough associations left to find. Activity ended")
				
				return (None, None)

		
		# select other "wrong" associations
		

		
		all_associations = copy.copy(good_associations)
		
		for i in range(amount_draggable - len(self.goals)) :
			
			found = False
			
			if (len(all_associations) >= len(self.associations)) :
				# we won't be able to find other associations (all are already selected)
				# so we have to stop, to avoid an infinite while loop below
				common.info("Not enough associations available for 'bad' choices.")
				common.info("Please check your xml file to add more associations or lower 'max_draggable' parameter")

				return (None, None)
				

			while (found == False) :
				other_association = self.associations[random.randint(0, len(self.associations)-1)]
				
				if (other_association not in all_associations) :
					all_associations.append(other_association)

					found = True


		
		
		# eventually sorting the entries
		if (self.sort == True) :
			all_associations.sort()
		else :
			all_associations = common.randomize_list(all_associations)

		
		return (good_associations, all_associations)

def next_page(game, globalvars) :
	# displays another page to play

	
	(good_association, all_associations) = game.get_random_associations()

	game.rounds_done = game.rounds_done + 1

	if ((good_association != None) and (game.rounds_done < game.rounds_amount + 1)) :

		current_page = Page_associate(game, globalvars, good_association, all_associations)

		current_page.fade_in()
		pygame.display.flip()
		
		if (cmp(game.music_mode, "off") == 0) :
			# if silence was requested (no music)
			# we make sure no more sound will be heard from previous page
			pygame.mixer.fadeout(constants.fadeout_sound_duration)

		current_page.game = game

		game.start_timer()

		return current_page
	
	else :
		common.info("No more associations to look for !")
	
		return None



class Run_Associate(common.Run_Screen) :

	def __init__(self, game, globalvars, total_score) :

		common.info("Running association game")
		
		game = Associate_game(game, globalvars.main_language, total_score)

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

					elif ((component_clicked.associated_object != None) and (self.mousebutton == 3)) :

						# right click on an item (draggable or to associate)
						# it will be displayed in big

						if (component_clicked not in self.current_page.goals) :
							association = component_clicked.associated_object

							if (component_clicked in self.current_page.items_to_associate) :
								(text, image_file, associated_sounds) = association.get_infos_for_display_big_to_associate()
							else :
								(text, image_file, associated_sounds) = association.get_infos_for_display_big_to_drag()

							if (image_file != None) :

								if (self.current_page.completed == False) :
									self.game.stop_timer()

								self.current_page.fade_out()

								display_big.Run_Display_Big(self.globalvars, text, image_file, associated_sounds)

								# redraw the whole screen
								self.current_page.draw()

								some_dirty_rects = [self.screen.get_rect()]

								self.mouse_clicked = False

								if (self.current_page.completed == False) :
									self.game.start_timer()


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


				####self.total_time = self.total_time + self.current_page.timer.getValue()


				self.current_page = next_page(self.game, globalvars)

				if (self.current_page == None) :
					return


			common.Run_Screen.run_post(self)	
