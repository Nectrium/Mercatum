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


import pygame, copy
from pygame.locals import *

import common, ui, constants, xml_funcs, i18n, random
	
class Page_transform(ui.Game_Page) :

	def __init__(self, globalvars, transformation, game) :

		self.transformation = transformation


		ui.Game_Page.__init__(self, globalvars, game)

	def update(self) :
		
		ui.Page.update(self)

		if (cmp(self.transformation.text, "") == 0) :
			text = self.game.get_title(self.language)
			
		else :
			text = self.transformation.text




		# load the original image
		common.info("Loading original image "+ self.transformation.original_image_filename)
		self.original_image = ui.Image(self, self.game.image_pos, self.game.image_size, self.transformation.original_image_filename)


		self.unveil_width = ((self.original_image.rect.width) / self.transformation.pieces_amount_x)
		self.unveil_height = ((self.original_image.rect.height) / self.transformation.pieces_amount_y)

		self.rounded_width = int(round(self.unveil_width * self.transformation.pieces_amount_x))
		self.rounded_height = int(round(self.unveil_height * self.transformation.pieces_amount_y))


		self.original_image.cliprect_abs=((self.original_image.x, self.original_image.y), (self.rounded_width, self.rounded_height))


		# in case the original_image has transparent alpha pixels
		original_image_surface_copy = copy.copy(self.original_image.surface)

		self.original_image.surface.blit(self.screen.subsurface(self.original_image.rect), (0,0) )

		self.original_image.surface.blit(original_image_surface_copy, (0,0))


		# add the "transformed" image
		common.info("Loading transformed image "+ self.transformation.transformed_image_filename)		
		(resized_image, foo) = ui.load_image(self.transformation.transformed_image_filename, (self.original_image.rect.width, self.original_image.rect.height), "FILL")

		self.image = ui.Image_Absolute(self, (self.original_image.rect.left, self.original_image.rect.top), (self.original_image.rect.width, self.original_image.rect.height), resized_image)


		self.append(self.image)
		self.image.cliprect_abs=((self.image.rect.left, self.image.rect.top), (self.rounded_width, self.rounded_height))



		# the "alpha" surfaces are transparent original images to make a smoother
		# transition between transformed and original image
		self.alpha_surfaces = []
		alpha_step = 255 / (self.transformation.amount_alpha_surfaces + 2)
		alpha_value = alpha_step

		self.transformed_surface = copy.copy(self.image.surface)

		for i in range(self.transformation.amount_alpha_surfaces) :

			alpha_surface = copy.copy(self.original_image.surface)
			alpha_surface.set_alpha(alpha_value)

			alpha_value = alpha_value + alpha_step

			self.alpha_surfaces.append(alpha_surface)









		self.transformation.init_table()


	
		
	def was_something_clicked(self, (x, y), mousebutton) :
	
		clicked = ui.Page.was_something_clicked(self, (x,y), mousebutton)		
	
		if (clicked != None) :
			(component_clicked, foo, dirty1) = clicked	
			

		return clicked

	def unveil(self, mouse_pos) :

		(mouse_x, mouse_y) = mouse_pos
		(mouse_x, mouse_y) = (mouse_x - self.image.rect.left, mouse_y - self.image.rect.top)

		coords_converter = ui.Coordinates_converter(self, Rect((0, 0), (self.image.rect.width, self.image.rect.height)), Rect((0,0), (self.transformation.pieces_amount_x, self.transformation.pieces_amount_y)))

		(x, y) = coords_converter.get_coords_px_org2px((mouse_x, mouse_y))

		(x, y) = (int(x), int(y))

		dirty_rect = None

		if (self.transformation.table[x][y] == False) :

			# start of black magic
			# TODO : fix graphical bugs (rewrite code ?)

			dest_x = x * self.unveil_width
			dest_y = y * self.unveil_height

			width = self.unveil_width
			height = self.unveil_height

			dirty_rect = Rect((dest_x, dest_y), (width, height))

			# do we have to draw the transitions or will it be a normal blit ?
			
			# top ?
			if (y > 0) :
				if (self.transformation.table[x][y-1] == False) :
					draw_top_transition = True
				else :
					draw_top_transition = False
			else :
				draw_top_transition = False

			# bottom ?
			if (y < self.transformation.pieces_amount_y - 1) :
				if (self.transformation.table[x][y+1] == False) :
					draw_bottom_transition = True
				else :
					draw_bottom_transition = False
			else :
				draw_bottom_transition = False

			# left ?
			if (x > 0) :
				if (self.transformation.table[x-1][y] == False) :
					draw_left_transition = True
				else :
					draw_left_transition = False
			else :
				draw_left_transition = False

			# right ?
			if (x < self.transformation.pieces_amount_x - 1) :
				if (self.transformation.table[x+1][y] == False) :
					draw_right_transition = True
				else :
					draw_right_transition = False
			else :
				draw_right_transition = False



			# drawing the alpha transition between the pictures
			for alpha in range(self.transformation.amount_alpha_surfaces) :
				
				# top line
				if (draw_top_transition == True) :
					self.image.surface.blit(self.alpha_surfaces[alpha], (dest_x, dest_y), ((dest_x, dest_y), (width, 1)))

					if (draw_left_transition == False) :

						if (x > 0) :

							# first we reset the alpha transformation there
							self.image.surface.blit(self.transformed_surface, (dest_x-self.transformation.amount_alpha_surfaces, dest_y), ((dest_x-self.transformation.amount_alpha_surfaces, dest_y), (self.transformation.amount_alpha_surfaces, 1)))

							self.image.surface.blit(self.alpha_surfaces[alpha], (dest_x-self.transformation.amount_alpha_surfaces, dest_y), ((dest_x-self.transformation.amount_alpha_surfaces, dest_y), (self.transformation.amount_alpha_surfaces, 1)))

					if (draw_right_transition == False) :
						
						if (x < self.transformation.pieces_amount_x - 1) :

							self.image.surface.blit(self.transformed_surface, (dest_x + width, dest_y), ((dest_x + width, dest_y), (self.transformation.amount_alpha_surfaces, 1)))

							self.image.surface.blit(self.alpha_surfaces[alpha], (dest_x + width, dest_y), ((dest_x + width, dest_y), (self.transformation.amount_alpha_surfaces, 1)))


				# bottom line
				if (draw_bottom_transition == True) :
					self.image.surface.blit(self.alpha_surfaces[alpha], (dest_x, dest_y+height-1), ((dest_x, dest_y+height-1), (width, 1)))

					if (draw_left_transition == False) :

						if (x > 0) :
		
							self.image.surface.blit(self.transformed_surface, (dest_x-self.transformation.amount_alpha_surfaces, dest_y+height-1), ((dest_x-self.transformation.amount_alpha_surfaces, dest_y+height-1), (self.transformation.amount_alpha_surfaces, 1)))

							self.image.surface.blit(self.alpha_surfaces[alpha], (dest_x-self.transformation.amount_alpha_surfaces, dest_y+height-1), ((dest_x-self.transformation.amount_alpha_surfaces, dest_y+height-1), (self.transformation.amount_alpha_surfaces, 1)))

					if (draw_right_transition == False) :
						
						if (x < self.transformation.pieces_amount_x - 1) :

							self.image.surface.blit(self.transformed_surface, (dest_x + width, dest_y+height-1), ((dest_x + width, dest_y+height-1), (self.transformation.amount_alpha_surfaces, 1)))

							self.image.surface.blit(self.alpha_surfaces[alpha], (dest_x + width, dest_y+height-1), ((dest_x + width, dest_y+height-1), (self.transformation.amount_alpha_surfaces, 1)))


				# left line
				if (draw_left_transition == True) :
					self.image.surface.blit(self.alpha_surfaces[alpha], (dest_x, dest_y+1), ((dest_x, dest_y+1), (1, height-2)))
					
					if (draw_top_transition == False) :

						self.image.surface.blit(self.transformed_surface, (dest_x, dest_y-1-self.transformation.amount_alpha_surfaces), ((dest_x, dest_y-1-self.transformation.amount_alpha_surfaces), (1, 2+ (2 * self.transformation.amount_alpha_surfaces))))

						self.image.surface.blit(self.alpha_surfaces[alpha], (dest_x, dest_y-1-self.transformation.amount_alpha_surfaces), ((dest_x, dest_y-1-self.transformation.amount_alpha_surfaces), (1, 2+ (2 * self.transformation.amount_alpha_surfaces))))

					if (draw_bottom_transition == False) :
						self.image.surface.blit(self.transformed_surface, (dest_x, dest_y+height-1-self.transformation.amount_alpha_surfaces), ((dest_x, dest_y+height-1-self.transformation.amount_alpha_surfaces), (1, 2+ (2 * self.transformation.amount_alpha_surfaces))))

						self.image.surface.blit(self.alpha_surfaces[alpha], (dest_x, dest_y+height-1-self.transformation.amount_alpha_surfaces), ((dest_x, dest_y+height-1-self.transformation.amount_alpha_surfaces), (1, 2+ (2 * self.transformation.amount_alpha_surfaces))))


				# right line
				if (draw_right_transition == True) :
					self.image.surface.blit(self.alpha_surfaces[alpha], (dest_x+width-1, dest_y+1), ((dest_x+width-1, dest_y+1), (1, height-2)))

					if (draw_top_transition == False) :
						self.image.surface.blit(self.transformed_surface, (dest_x+width-1, dest_y-1-self.transformation.amount_alpha_surfaces), ((dest_x+width-1, dest_y-1-self.transformation.amount_alpha_surfaces), (1, 2+ (2 * self.transformation.amount_alpha_surfaces))))

						self.image.surface.blit(self.alpha_surfaces[alpha], (dest_x+width-1, dest_y-1-self.transformation.amount_alpha_surfaces), ((dest_x+width-1, dest_y-1-self.transformation.amount_alpha_surfaces), (1, 2+ (2 * self.transformation.amount_alpha_surfaces))))

					if (draw_bottom_transition == False) :
						self.image.surface.blit(self.transformed_surface, (dest_x+width-1, dest_y+height-1-self.transformation.amount_alpha_surfaces), ((dest_x+width-1, dest_y+height-1-self.transformation.amount_alpha_surfaces), (1, 2+ (2 * self.transformation.amount_alpha_surfaces))))

						self.image.surface.blit(self.alpha_surfaces[alpha], (dest_x+width-1, dest_y+height-1-self.transformation.amount_alpha_surfaces), ((dest_x+width-1, dest_y+height-1-self.transformation.amount_alpha_surfaces), (1, 2+ (2 * self.transformation.amount_alpha_surfaces))))



				if (draw_top_transition == True) :
					dest_y = dest_y + 1

				if (draw_left_transition == True) :
					dest_x = dest_x + 1




				if (draw_top_transition == True) :
					height = height - 1

				if (draw_bottom_transition == True) :
					height = height - 1

				if (draw_left_transition == True) :				
					width = width - 1
			
				if (draw_right_transition == True) :	
					width = width - 1




			if (draw_top_transition == False) :
				
				if (y > 0) :
					dest_y = dest_y - self.transformation.amount_alpha_surfaces
					dirty_rect.top = dirty_rect.top - self.transformation.amount_alpha_surfaces
					height = height + self.transformation.amount_alpha_surfaces
					dirty_rect.height = dirty_rect.height + self.transformation.amount_alpha_surfaces
				dest_y = dest_y - self.transformation.amount_alpha_surfaces
				height = height + self.transformation.amount_alpha_surfaces

				#self.image.surface.blit(self.original_image.surface, (dest_x, dest_y), ((dest_x, dest_y), (width, height)))
			
			if (draw_bottom_transition == False) :
				if (y < self.transformation.pieces_amount_y - 1) :
					height = height + self.transformation.amount_alpha_surfaces
					dirty_rect.height = dirty_rect.height + self.transformation.amount_alpha_surfaces	
				height = height + self.transformation.amount_alpha_surfaces

			if (draw_left_transition == False) :
				if (x > 0) :
					dest_x = dest_x - self.transformation.amount_alpha_surfaces
					dirty_rect.left = dirty_rect.left - self.transformation.amount_alpha_surfaces
					width = width + self.transformation.amount_alpha_surfaces
					dirty_rect.width = dirty_rect.width + self.transformation.amount_alpha_surfaces
				dest_x = dest_x - self.transformation.amount_alpha_surfaces
				width = width + self.transformation.amount_alpha_surfaces

			if (draw_right_transition == False) :
				if (x < self.transformation.pieces_amount_x - 1) :
					width = width + self.transformation.amount_alpha_surfaces
					dirty_rect.width = dirty_rect.width + self.transformation.amount_alpha_surfaces
				width = width + self.transformation.amount_alpha_surfaces

			#dest_x = dest_x + self.transformation.amount_alpha_surfaces
			#dest_y = dest_y + self.transformation.amount_alpha_surfaces

			#width = self.unveil_width - 2 * self.transformation.amount_alpha_surfaces
			#height = self.unveil_height - 2 * self.transformation.amount_alpha_surfaces


			# we change the surface of the component
			self.image.surface.blit(self.original_image.surface, (dest_x, dest_y), ((dest_x, dest_y), (width, height)))

			dirty_rect = dirty_rect.move(self.image.rect.topleft)

			# and then we redraw this part of the component
			self.image.cliprect_abs = dirty_rect
			
			self.image.draw()

			self.image_cliprect_abs = None


			self.transformation.table[x][y] = True

			self.transformation.amount_left_to_unveil = self.transformation.amount_left_to_unveil - 1


			if (self.transformation.amount_left_to_unveil <= 0) :
				self.transformation.done = True
				self.completed = True
				self.play_congratulations_sound()	

				self.append(self.next_icon)
				self.next_icon.draw()

				dirty_rect = self.screen.get_rect()

		return [dirty_rect]




class Transformation() :
	def __init__(self, game) :
		self.game = game

		self.transformed_image_filename = ""
		self.original_image_filename = ""

		self.text = ""

		self.done = False
		
		self.pieces_amount_x = 0
		self.pieces_amount_y = 0

		self.table = None

		self.amount_left_to_unveil = None

		# TODO make this a variable in XML game file
		self.amount_alpha_surfaces = 5


	def init_table(self) :
		# the 'table' contains all the cells which have to be transformed

		self.table = []
		for x in range(self.pieces_amount_x) :
			column = []
			for y in range(self.pieces_amount_y) :
				column.append(False)
			self.table.append(column)
				

		self.amount_left_to_unveil = (self.pieces_amount_x * self.pieces_amount_y)


		
class Transform_game(common.Game) :

	def __init__(self, game, lang) :

		self.globalvars = game.globalvars
		
		# creation of a new game
		common.Game.__init__(self, self.globalvars, game.xml_game_node, game.level)

		if (self.xml_game_node != None) :

			# reading global parameters
			xml_global_parameters_node = self.xml_game_node.getElementsByTagName("global_parameters")[0]
		
			# first of all, game setup
			xml_game_setup_node = self.xml_game_node.getElementsByTagName("game_setup")[0]
			
			# the default amount of pieces on x and y axis
			self.pieces_amount_x = xml_funcs.getInt(xml_game_setup_node.getElementsByTagName("pieces_amount_x")[0])
			self.pieces_amount_y = xml_funcs.getInt(xml_game_setup_node.getElementsByTagName("pieces_amount_y")[0])

			# area for image :
			image_area_node = xml_global_parameters_node.getElementsByTagName("image_area")[0]
			(self.image_pos, self.image_size) = xml_funcs.get_box(image_area_node)

			
			# reading transformation items
			
			main_transformations = self.xml_game_node.getElementsByTagName("transformations")[0]
			
			transformation_nodes = main_transformations.getElementsByTagName("transformation")
			
			self.transformations = []
			
			for transformation_node in transformation_nodes :
				
				transformation = Transformation(self)
				
				image_nodes = transformation_node.getElementsByTagName("image")


				# TODO : make this a bit more robust ?
				transformation.transformed_image_filename = xml_funcs.getText(image_nodes[0])
				transformation.original_image_filename = xml_funcs.getText(image_nodes[1])


				text_nodes = transformation_node.getElementsByTagName("text")
				
				if len(text_nodes) > 0 :
					
					for text_node in text_nodes :

						lang_attr = text_node.getAttribute("lang")
						
						if (lang_attr == "") :
							# if no "lang" attribute, we assume
							# the language of the text is the one expected
							transformation.text = xml_funcs.getText(text_node)
						
						if (cmp(lang_attr, lang) == 0) :
							# if we have the correct language, we
							# take the text and exit the loop
							transformation.text = xml_funcs.getText(text_node)
							break
					
				if (transformation.pieces_amount_x == 0) :
					transformation.pieces_amount_x = self.pieces_amount_x
				
				if (transformation.pieces_amount_y == 0) :
					transformation.pieces_amount_y = self.pieces_amount_y
					
				self.transformations.append(transformation)
				
			self.transformations = common.randomize_list(self.transformations)
	
	def get_transformation(self) :
		# returning an image to transform
		for transformation in self.transformations :
			if (transformation.done == False) :
				return transformation
		else :
			# no more transformations to do
			return None


def next_page(current_page, game, globalvars) :

	next_transformation = game.get_transformation()
	
	game.rounds_done = game.rounds_done + 1
	
	if ((next_transformation <> None) and (game.rounds_done < game.rounds_amount)) :
		
		current_page.fade_out()
		
		current_page = Page_transform(globalvars, next_transformation, game)
	
		current_page.draw()
		pygame.display.flip()

		return current_page

	else :
		common.info("Game over: no more transformations !")
		
		return None


class Run_Transform_Screen(common.Run_Screen) :

	def __init__(self, game, globalvars) :
	
		common.info("Running transformation activity")

		game = Transform_game(game, globalvars.main_language)

		common.Run_Screen.__init__(self, globalvars, game)	

		self.current_page = Page_transform(globalvars, self.game.get_transformation(), self.game)
	
		self.current_page.draw()
		pygame.display.flip()
	

		while self.running :

			common.Run_Screen.run_pre(self)

			# actions after keyboard events

			for key_event in self.key_events :
								
				if key_event.key == K_SPACE :
					if (self.current_page.transformation.done == True) :
						self.current_page = next_page(self.current_page, self.game, globalvars)
						if (self.current_page == None) :
							return
	
			# actions for mouse actions
			if (self.mouse_clicked == True) :
			
				clicked = self.current_page.was_something_clicked(self.mouse_pos, self.mousebutton)
		
				if (clicked != None) :
					(component_clicked, xml_file, some_dirty_rects) = clicked

					if (component_clicked == self.current_page.quit_icon) :
						raise common.EndActivityException()

					elif (component_clicked == self.current_page.next_icon) :
						self.current_page = next_page(self.current_page, self.game, globalvars)

						if (self.current_page == None) :
							return
		
					self.dirty_rects = self.dirty_rects + some_dirty_rects

			
			# let's see if we have some image part to unveil
	
			mouse_pos = pygame.mouse.get_pos()

			if (self.current_page.image.rect.collidepoint(mouse_pos)) :
				self.dirty_rects = self.dirty_rects + self.current_page.unveil(mouse_pos)


		
			common.Run_Screen.run_post(self)
		
