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

import pygame, sys, os, random, datetime
from pygame.locals import *
			
import ui, constants, common


class Page_igloo(ui.Page) :


	def __init__(self, globalvars) :
		
		self.dragged_sprite = None
		self.draggable_items = []
	
		background = constants.igloo_background_file
	
		self.find_tuxes()
	
		self.tux_going_out = None

		ui.Page.__init__(self, globalvars, background)

	def init_background(self) :

		# the background of the igloo is indeed a part of the menu background image

		common.info("Init igloo background - start")

 		(surface, dim) = ui.load_image(constants.main_menu_back)

		(surface_x_pc, surface_y_pc) = constants.igloo_pos

		surface_x = int((surface_x_pc * surface.get_width()) / 100)
		surface_y = int((surface_y_pc * surface.get_height()) / 100)

		(surface_width_pc, surface_height_pc) = constants.igloo_size

		surface_width = int((surface_width_pc * surface.get_width()) / 100)
		surface_height = int((surface_height_pc * surface.get_height()) / 100)


		self.surface_to_zoom_rect = Rect(surface_x, surface_y, surface_width, surface_height)

		surface_to_zoom = surface.subsurface(self.surface_to_zoom_rect)

		self.background = pygame.transform.scale(surface_to_zoom, (self.screen.get_width(), self.screen.get_height()))
		
		# now let's go back to screen dimensions :
		surface_x = int(self.x_pc2px(surface_x_pc))
		surface_y = int(self.y_pc2px(surface_y_pc))

		surface_width = int(self.x_pc2px(surface_width_pc))
		surface_height = int(self.y_pc2px(surface_height_pc))

		self.surface_to_zoom_rect = Rect(surface_x, surface_y, surface_width, surface_height)

		
		# adding the igloo
		self.igloo = ui.Image(self, (0,0), (100,100), constants.igloo_file, 255, 100, "TOPLEFT")
		
		self.append_back(self.igloo)

		# not clean, but same trick as used in ui.Page.draw_back()
		save_screen = self.screen
		self.screen = self.background
		self.igloo.draw()
		self.screen = save_screen

		(foo, initial_width, initial_height) = ui.get_image_info(constants.igloo_file)
		coord_convert_igloo = ui.Coordinates_converter(self, Rect((0,0), (initial_width, initial_height)), self.igloo.rect)
		
		# not very clean: as the limit is the height
		# we assume width could be three times as big (for instance !)
		self.tux_size = coord_convert_igloo.get_coords_px2pc((3 * constants.tux_height, constants.tux_height))

		self.tux_initial_pos = coord_convert_igloo.get_coords_px2pc(constants.tux_initial_pos)

		(self.flag_mast_pos_x, self.flag_mast_pos_y) = coord_convert_igloo.get_coords_px2pc((constants.flag_mast_pos_x_px, 0))


		common.info("Init igloo background - before reducing")

		self.igloo_reduced_surface = pygame.transform.scale(self.background, self.surface_to_zoom_rect.size)

		common.info("Init igloo background - end")

	def update_igloo_reduced_surface(self) :

		self.igloo_reduced_surface = pygame.transform.scale(self.screen, self.surface_to_zoom_rect.size)
	
	def update(self) :
		
		ui.Page.update(self)

		self.init_background()

		self.next_icon = ui.Image(self, constants.go_next_icon_pos, constants.go_next_icon_size, constants.go_next_icon)

	def was_something_clicked(self, (x, y), mousebutton) :
	
		clicked = ui.Page.was_something_clicked(self, (x,y), mousebutton)		
	
		if (clicked != None) :
			(component_clicked, foo, dirty1) = clicked	
			
			if (self.dragged_sprite == None) :
				# this might be a text to drag 
				
				for draggable_item in self.draggable_items :
					
					if (component_clicked == draggable_item) :
	
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
	
	def find_tuxes(self) :
		
		tuxes = common.get_files(constants.folder_award_tuxes, constants.image_extensions)
		
		self.tuxes = common.randomize_list(tuxes)
		
	
	def new_tux(self) :
	
		# TODO: the tuxes should go out from the igloo door
	
		index = random.randint(0, len(self.tuxes)-1)
		image_file = self.tuxes[index]
		self.tuxes.remove(image_file)
		
		
		self.tux_going_out = ui.Image(self, self.tux_initial_pos, self.tux_size , image_file)
	
		(width, height) = self.tux_size
	
		x_delta = (self.x_pc2px(width) - self.tux_going_out.rect.width) / 2
		self.goal_tux_x = self.tux_going_out.rect.left - x_delta
		
		y_delta = self.y_pc2px(height) - self.tux_going_out.rect.height
		
		self.tux_going_out.rect.left = self.tux_going_out.rect.left - x_delta - self.tux_going_out.rect.width
		self.tux_going_out.rect.top = self.tux_going_out.rect.top + y_delta
	
		self.tux_going_out.set_cliprect((self.tux_initial_pos, self.tux_size))
	
		self.append(self.tux_going_out)
	

	
	def tux_goes_out(self) :
		
		if (self.tux_going_out != None) :
		
			if (self.tux_going_out.rect.left < self.goal_tux_x) :
				self.tux_going_out.rect.left = self.tux_going_out.rect.left + constants.tux_speed
	
				return self.tux_going_out.erase() + self.tux_going_out.draw()
			
			else :
				self.tux_going_out.set_cliprect(((0,0), (100,100)))
				
				self.draggable_items.append(self.tux_going_out)
				
				self.tux_going_out = None
				
				self.append(self.next_icon)	
				
				return self.next_icon.draw()
		


def create(globalvars) :

	igloo_page = Page_igloo(globalvars)	
	
	return igloo_page


class Run_Igloo(common.Run_Screen) :

	def __init__(self, igloo_page) :

		common.info("Running Igloo")

		self.current_page = igloo_page

		common.Run_Screen.__init__(self, self.current_page.globalvars)	
		
		if (igloo_page.tux_going_out != None) :
			if (igloo_page.next_icon in igloo_page.items) :

				igloo_page.mouse_sprite.background = None

				igloo_page.remove(igloo_page.next_icon)
		else :
			if (igloo_page.next_icon not in igloo_page.items) :
				igloo_page.append(igloo_page.next_icon)		
		
		igloo_page.draw()
		pygame.display.flip()
		

		while (self.running or igloo_page.tux_going_out != None) :

			try :

				common.Run_Screen.run_pre(self)

			except common.EndActivityException, e :
				if (igloo_page.tux_going_out == None) :
					self.running = False
	
	
			# actions for mouse actions
			if (self.mouse_clicked == True) :
			
				clicked = igloo_page.was_something_clicked(self.mouse_pos, self.mousebutton)
					
				if (clicked != None) :
					(component_clicked, foo, some_dirty_rects) = clicked

					self.dirty_rects = self.dirty_rects + some_dirty_rects
						
					if (component_clicked == igloo_page.next_icon) :
						self.running = False
						
			# actions for keyboard
			for key_event in self.key_events :

				if (key_event.key == K_SPACE) :		
				
					if (igloo_page.tux_going_out == None):
						# we quit only after the tux has left the igloo !
						self.running = False
		
						
			if (igloo_page.tux_going_out != None) :
				self.dirty_rects = self.dirty_rects + igloo_page.tux_goes_out()
							

			common.Run_Screen.run_post(self)


		# cleaning the screen before the screenshot for menu : removal of 'next' button and mouse pointer
		self.dirty_rects = igloo_page.mouse_sprite.erase()
		self.dirty_rects = self.dirty_rects + igloo_page.remove(igloo_page.next_icon)
		pygame.display.update(self.dirty_rects)	

		igloo_page.update_igloo_reduced_surface()

