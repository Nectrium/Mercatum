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

import pygame, random, copy
from pygame.locals import *
			
import ui, constants, xml_funcs, i18n, common

class Page_differences(ui.Game_Page) :


	def __init__(self, game, globalvars) :
		
		
		# completed becomes True when all differences have been found
		self.completed = False
		
		self.differences_to_find_components = []

		ui.Game_Page.__init__(self, globalvars, game)

	
	def update(self) :
		
		ui.Page.update(self)
		

		# showing the pictures for differences
		(pos_original, size_original) = self.game.original_box
		self.original_image = ui.Image(self, pos_original, size_original, self.game.original_image_file)
		
		self.append(self.original_image)

		(pos_modified, size_modified) = self.game.modified_box
		self.modified_image = ui.Image(self, pos_modified, size_modified, self.game.modified_image_file)

		if ((self.game.original_width != None) and (self.game.original_height != None)) :
			self.modified_image.original_size = (self.game.original_width, self.game.original_height)


		# masking some differences
		for difference_to_mask in self.game.differences_to_mask :
			difference_to_mask.mask_difference(self.modified_image, self.original_image)
		
		self.append(self.modified_image)


		# components which have to be found
		for difference_to_find in self.game.differences_to_find :

			difference_to_find_component = difference_to_find.create_component_to_find(self)
		
			self.append(difference_to_find_component)
			self.differences_to_find_components.append(difference_to_find_component)

		# memorize number of differences to find and show display
		self.number_differences_to_find = len(self.differences_to_find_components)
		self.number_differences_found = 0
		text_number_differences = '%(found)d / %(tofind)d' %{'found' : self.number_differences_found, 'tofind' : self.number_differences_to_find}
                self.text_number_differences = ui.Text(self, text_number_differences, (46, 46), (8, 8), self.fonts, constants.text_color, 1)
                self.append(self.text_number_differences)

		self.draw_back()


	def was_something_clicked(self, (x, y), mousebutton) :
	
		clicked = ui.Page.was_something_clicked(self, (x,y), mousebutton)		
		
		if (clicked != None) :
			(component_clicked, foo, some_dirty_rects) = clicked

			# we try to play an associated sound (if any)
			component_clicked.play_random_associated_sound()

			if (component_clicked in self.differences_to_find_components) :
                                # a differences was found
				dirty_rects = []

				self.play_congratulations_sound()

				diff = component_clicked.associated_object

				found_component = diff.create_found_component(self, component_clicked)
				
				self.append(found_component)

				self.differences_to_find_components.remove(component_clicked)

                                # increase number of found differences and update display
                		self.number_differences_found += 1
                		text_number_differences = '%(found)d / %(tofind)d' %{'found' : self.number_differences_found, 'tofind' : self.number_differences_to_find}
				dirty_rects = dirty_rects + self.text_number_differences.erase()                                
				self.text_number_differences.set_text(text_number_differences)
                                self.text_number_differences.update()
                                dirty_rects = dirty_rects + self.text_number_differences.draw()

				# no need to redraw below the deleted box as it was transparent
				self.remove(component_clicked)

				dirty_rects = dirty_rects + found_component.draw()

				if (len(self.differences_to_find_components) == 0) :
					self.completed = True


				if (self.completed == True) :

					self.append(self.next_icon)

					self.game.stop_timer()

					dirty_rects = dirty_rects + self.next_icon.draw()


				return (component_clicked, foo, dirty_rects)
	
		return clicked

class Differences_game(common.Game) :

	def __init__(self, game, score) :

		self.globalvars = game.globalvars
		
		# creation of a new game
		common.Game.__init__(self, self.globalvars, game.xml_game_node, game.level, score)

		self.score.enable_record_time()


		if (self.xml_game_node != None) :

			# reading global parameters
			xml_global_parameters_node = self.xml_game_node.getElementsByTagName("global_parameters")[0]
		
			# the min and max amounts of differences to find
			self.min_differences = xml_funcs.getInt(xml_global_parameters_node.getElementsByTagName("min_differences")[0])
			self.max_differences = xml_funcs.getInt(xml_global_parameters_node.getElementsByTagName("max_differences")[0])

			# original image
			original_node  = xml_global_parameters_node.getElementsByTagName("original")[0]
			self.original_box = xml_funcs.get_box(original_node)
			
			original_image_file_node = original_node.getElementsByTagName("image")[0]
			self.original_image_file = xml_funcs.getText(original_image_file_node)


			# modified image
			modified_node  = xml_global_parameters_node.getElementsByTagName("modified")[0]
			self.modified_box = xml_funcs.get_box(modified_node)
			
			modified_image_file_node = modified_node.getElementsByTagName("image")[0]
			self.modified_image_file = xml_funcs.getText(modified_image_file_node)

			# original image size (useful for resized .light images)
			image_resolution_nodes = xml_global_parameters_node.getElementsByTagName("image_resolution")
			if (len(image_resolution_nodes) > 0) :

				image_resolution_node = image_resolution_nodes[0]

				self.original_width = float(image_resolution_node.getAttribute("width"))
				self.original_height = float(image_resolution_node.getAttribute("height"))

			else :
				# will be useful in case of an XML file with difference pos and size in percents and not pixels
				self.original_width = None
				self.original_height = None


			# images 'showing' the differences
			found_nodes = xml_global_parameters_node.getElementsByTagName("found")[0]

			self.found_file_names = []

			found_file_nodes = found_nodes.getElementsByTagName("image")

			for found_file_node in found_file_nodes :

				self.found_file_names.append(xml_funcs.getText(found_file_node))


			ratio_x_nodes = xml_global_parameters_node.getElementsByTagName("ratio_x")
			if (len(ratio_x_nodes) > 0) :
				self.ratio_x = (xml_funcs.getFloat(ratio_x_nodes[0])) / 100.0
			else :
				self.ratio_x = 1.0


			ratio_y_nodes = xml_global_parameters_node.getElementsByTagName("ratio_y")
			if (len(ratio_y_nodes) > 0) :
				self.ratio_y = (xml_funcs.getFloat(ratio_y_nodes[0])) / 100.0
			else :
				self.ratio_y = 1.0

			# reading differences
	
			main_differences_node = self.xml_game_node.getElementsByTagName("differences")[0]
			
			differences_nodes = main_differences_node.getElementsByTagName("difference")
			
			self.differences = []
			
			for difference_node in differences_nodes :
				
				difference = Difference(self, difference_node)
				
				self.differences.append(difference)

			if (len(self.differences) < self.max_differences) :
				common.error("The XML file contains " + str(len(self.differences)) + " differences")
				common.error("But at least "+self.max_differences + " differences are required")
				common.error("set up more differences or change the max_differences value")
				raise common.BadXMLException()

			

	def select_random_differences(self) :

		# the differences which will have to be found by the user
		self.differences_to_find = []

		# the differences which will be masked (copy the rect from the original image)
		self.differences_to_mask = []

		self.differences = common.randomize_list(self.differences)
		
		self.amount_differences = self.min_differences + random.randint(0, self.max_differences-self.min_differences)

		if (len(self.differences) < self.amount_differences) :
			common.error("Not enough differences available. Please check your XML setup : the value of the 'max_differences' tag is too high.")

			raise common.BadXMLException()


		for i in range(self.amount_differences) :

			difference = self.differences[0]

			self.differences.remove(self.differences[0])

			self.differences_to_find.append(difference)

		# at this point, only differences which have to be masked are yet in the self.differences list
		self.differences_to_mask = self.differences


class Difference() :

	def __init__(self, game, difference_node) :
	
		self.game = game

		self.difference_box = xml_funcs.get_box(difference_node)

	def create_component_to_find(self, page) :

		(difference_pos, difference_size) = self.difference_box

		# TODO : implement other modes than pixels relative to original image ?

		(pos_x, pos_y) = difference_pos
		(width, height) = difference_size

		delta_x = (width * (1 - self.game.ratio_x)) / 2.0
		delta_y = (height * (1 - self.game.ratio_y)) / 2.0

		difference_pos = (pos_x + delta_x, pos_y + delta_y)
		difference_size = (width * self.game.ratio_x, height * self.game.ratio_y)

		coords_converter = ui.Coordinates_converter(page, Rect((0,0), page.modified_image.original_size), page.modified_image.rect)

		difference_pos = coords_converter.get_coords_px2pc(difference_pos)
		difference_size = coords_converter.get_size_px2pc(difference_size)

		# component =  ui.Box(page, difference_pos, difference_size, constants.box_color, 100)

		# the trick is that the box is invisible (alpha = 0)
		# yet the player can click on it
		component = ui.Box(page, difference_pos, difference_size, constants.box_color, 0)

		component.set_associated_object(self)

		return component


	def create_found_component(self, page, component) :

		(difference_pos, difference_size) = ((component.x_percent, component.y_percent), (component.width_percent, component.height_percent))

		found_image_file = self.game.found_file_names[random.randint(0, len(self.game.found_file_names) - 1)]

		found_component = ui.Image(page, difference_pos, difference_size, found_image_file, 255, 100.0 , "FILL")

		return found_component



	def mask_difference(self, modified_image, original_image) :

		(difference_pos, difference_size) = self.difference_box

		# TODO : implement other modes than pixels relative to original image ?
		coords_converter = ui.Coordinates_converter(None, Rect((0,0), modified_image.original_size), Rect((0,0), modified_image.rect.size))

		difference_pos = coords_converter.get_coords_px_org2px(difference_pos)
		difference_size = coords_converter.get_size_px_org2px(difference_size)

		difference_rect = Rect(difference_pos, difference_size)

		#pygame.draw.rect(modified_image.surface, pygame.Color("red"), rect, 1)
		
		modified_image.surface.blit(original_image.surface.subsurface(difference_rect), difference_rect)
		


class Run_Differences_Screen(common.Run_Screen) :

	def __init__(self, game, globalvars, total_score) :

		common.info("Running differences activity")

		game = Differences_game(game, total_score)
		
		game.select_random_differences()

		common.Run_Screen.__init__(self, globalvars, game)

		self.current_page = Page_differences(self.game, globalvars)
		
		self.current_page.draw()
		
		pygame.display.flip()

		game.start_timer()

		while self.running :

			common.Run_Screen.run_pre(self)

			# actions after keyboard events

			for key_event in self.key_events :
								
				if key_event.key == K_SPACE :
					if (self.current_page.completed == True) :
						self.running = False


				
			if (self.mouse_clicked == True) :
				
				clicked = self.current_page.was_something_clicked(self.mouse_pos, self.mousebutton)
					
				if (clicked != None) :
					(component_clicked, foo, some_dirty_rects) = clicked
		
					if (component_clicked == self.current_page.quit_icon) :
						raise common.EndActivityException()

					elif (component_clicked == self.current_page.next_icon) :
						self.running = False

					self.dirty_rects = self.dirty_rects + some_dirty_rects

			common.Run_Screen.run_post(self)


		

