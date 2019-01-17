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

import common, ui, constants, xml_funcs, i18n

class Page_basic_puzzle(ui.Game_Page) :

	def __init__(self, globalvars, puzzle, game) :

		self.puzzle = puzzle
		
		self.puzzle_file = self.puzzle.image
		
		self.height_percent_puzzle = 92.0
		self.start_posy_puzzle_percent = 7.0
	
		self.ratio_spacing_pieces_y = 1.10 # grow factor on the y axis
		self.ratio_spacing_pieces_x = 1.10
	
		self.pieces_amount_x = self.puzzle.pieces_amount_x
		self.pieces_amount_y = self.puzzle.pieces_amount_y
		
		self.tux_size_ratio_percent = 70
		self.alpha_tux = 50
		
		self.drag_precision = 0.8				
		
		ui.Game_Page.__init__(self, globalvars, game)

	def update(self) :
		
		ui.Page.update(self)

		(image_type, width, height) = ui.get_image_info(self.puzzle_file)

	
	
		self.game_area_width = self.screen.get_width()
		self.game_area_height = (self.screen.get_height()*self.height_percent_puzzle) // 100
	
		self.start_posy_puzzle = (self.start_posy_puzzle_percent * self.screen.get_height()) // 100
	
		max_width = self.game_area_width
		max_height = self.game_area_height	
	
		if ((width < max_width) and (height < max_height)) :
			ratio = (height*1.0) / width
			
			width = max_width
			height = ratio * width	
			
		amount_pieces = 0
	
		while (amount_pieces < self.pieces_amount_x * self.pieces_amount_y) :
			max_width = max_width * 0.97
			max_height = max_height * 0.98
			
			if (width > max_width) :
				# we must keep proportions so we have to change the height...
				new_height = (height * max_width) // width
				new_width = max_width
						
			elif (height > max_height) :
				# we must keep proportions so we have to change the width...
				new_width = (width * max_height) // height
				new_height = max_height	
		
			else :
				new_width = width
				new_height = height
			
		
			# puzzle looks like this :
			#
			#  OOO PPPPP OOO
			#  OOO PPPPP OOO
			#  OOO PPPPP OOO
			#  OOOOOOOOOOOOO
			#  OOOOOOOOOOOOO
			#
			# O = a piece
			# P = the puzzle itself
			
			piece_space_x = (new_width * self.ratio_spacing_pieces_x) // self.pieces_amount_x
			piece_space_y = (new_height * self.ratio_spacing_pieces_y) // self.pieces_amount_y
			
			usable_x_top = (self.game_area_width - new_width)//2
			amount_x_pieces_top = usable_x_top // piece_space_x
			
			#print "amount_x_pieces_top " + str(amount_x_pieces_top)	
			
			usable_y_top = new_height
			amount_y_pieces_top = usable_y_top // piece_space_y
	
			#print "amount_y_pieces_top " + str(amount_y_pieces_top)	
	
			usable_x_bottom = self.game_area_width
			amount_x_pieces_bottom = usable_x_bottom // piece_space_x
			
			#print "amount_x_pieces_bottom " + str(amount_x_pieces_bottom)		
			
			usable_y_bottom = self.game_area_height - new_height
			amount_y_pieces_bottom = usable_y_bottom // piece_space_y
			
			#print "amount_y_pieces_bottom " + str(amount_y_pieces_bottom)
			
			amount_pieces = (2 * (amount_x_pieces_top * amount_y_pieces_top)) + (amount_x_pieces_bottom * amount_y_pieces_bottom)
			
			#print "amount_pieces " + str(amount_pieces)
		
		
		(resized_bitmap, foo) = ui.load_image(self.puzzle_file, (new_width, new_height))
		
		new_width = resized_bitmap.get_width()
		new_height = resized_bitmap.get_height()
	
		if (amount_y_pieces_top == 0) :
			amount_x_pieces_top = 0
			
		if (amount_x_pieces_top == 0) :
			amount_y_pieces_top = 0
	
		
		self.puzzle_image = ui.Image_Absolute(self, ((self.screen.get_width()-new_width) // 2, self.start_posy_puzzle), (new_width, new_height), resized_bitmap)	
		
		piece_size_x = new_width  // self.pieces_amount_x
		piece_size_y = new_height // self.pieces_amount_y
			
		rel_x = -1
		rel_y = 1
		
		delta_x = (piece_space_x - piece_size_x) // 2
		
		delta_y = (piece_space_y - piece_size_y) // 2

		self.puzzle_pieces = []
		self.tuxes = []		
		self.empty_locations = []
		
		for x in range(self.pieces_amount_x) :
			x_pos = x * piece_size_x
			for y in range(self.pieces_amount_y) :
				y_pos = y * piece_size_y
				
				size_x = piece_size_x
				size_y = piece_size_y
	
				if ((x == self.pieces_amount_x - 1) and (x_pos + piece_size_x > self.puzzle_image.surface.get_width())) :
					size_x = self.puzzle_image.surface.get_width() - x_pos
						
				if ((y == self.pieces_amount_y - 1) and (y_pos + piece_size_y > self.puzzle_image.surface.get_height())) :
					size_y = self.puzzle_image.surface.get_height() - y_pos
						
				if (rel_y <= amount_y_pieces_top) :
					# we are in the top part, on the left and right of the finished puzzle
					if (rel_x < 0) :
						# on the left of the finished puzzle
						x_piece_pos = self.puzzle_image.rect.centerx + rel_x * piece_space_x - self.puzzle_image.surface.get_width() // 2
					else :
						# on the right of the finished puzzle
						x_piece_pos = self.puzzle_image.rect.centerx + (rel_x - 1) * piece_space_x + self.puzzle_image.surface.get_width() // 2
					
					y_piece_pos = self.puzzle_image.rect.bottom - (rel_y  * piece_space_y)
				
				else :
					# we are below the finished puzzle
					if (rel_x < 0) :
						if (amount_x_pieces_bottom % 2 == 0) :
							x_piece_pos = self.puzzle_image.rect.centerx + (rel_x  * piece_space_x)
						else :
							x_piece_pos = self.puzzle_image.rect.centerx + ((rel_x+0.5)  * piece_space_x)
					else :
						if (amount_x_pieces_bottom % 2 == 0) :
							x_piece_pos = self.puzzle_image.rect.centerx + ((rel_x-1)  * piece_space_x) 
						else :
							x_piece_pos = self.puzzle_image.rect.centerx + ((rel_x-0.5)  * piece_space_x) 
					
					y_piece_pos = self.puzzle_image.rect.bottom + ((rel_y - 1 - amount_y_pieces_top) * piece_space_y)				
					
					
					
	
				
				if (rel_x < 0) :
					rel_x = -rel_x
	
					if ((amount_x_pieces_bottom % 2 == 1) and (rel_x > amount_x_pieces_bottom // 2) and (rel_y > amount_y_pieces_top)) :
						rel_x = -1
						rel_y = rel_y + 1
	
				else :
					rel_x = - (rel_x + 1)
					
					if (((rel_y <= amount_y_pieces_top) and (rel_x < -amount_x_pieces_top)) or ((amount_x_pieces_bottom % 2 == 0) and (rel_x < -(amount_x_pieces_bottom // 2)) and (rel_y > amount_y_pieces_top))) :	
							rel_y = rel_y + 1
							rel_x = -1
				
						

						
						
				empty_location = ui.Empty_Box_Absolute(self, (x_pos + self.puzzle_image.rect.left, y_pos + self.puzzle_image.rect.top), (size_x, size_y), constants.line_color, constants.line_alpha)
				
				self.append_back(empty_location)
				
				self.empty_locations.append(empty_location)
				
				
				
				((tux_x_percent, tux_y_percent), (tux_width_percent, tux_height_percent)) = ( \
				(self.x_px2pc(x_pos + self.puzzle_image.rect.left), self.y_px2pc(y_pos + self.puzzle_image.rect.top)), \
				(self.x_px2pc(size_x), self.y_px2pc(size_y)))



				
				tux = ui.Image(self, (tux_x_percent, tux_y_percent), (tux_width_percent, tux_height_percent), self.game.goal_image_file, self.alpha_tux, self.tux_size_ratio_percent)
				
				self.append_back(tux)
				
				self.tuxes.append(tux)
				
				
				
				piece_image = ui.Image_Absolute(self, (x_piece_pos + delta_x, y_piece_pos + delta_y), (size_x, size_y), resized_bitmap.subsurface(Rect((x_pos, y_pos), (size_x, size_y))))
				
				piece_image.set_associated_object(empty_location)
				
				self.append(piece_image)
								
				self.puzzle_pieces.append(piece_image)
				

		common.randomize_rects(self.puzzle_pieces)

		common.center_vert_absolute(self.puzzle_pieces + self.tuxes + self.empty_locations, self.start_posy_puzzle, self.game_area_height)

		if (cmp(self.puzzle.text, "") == 0) :

			text = self.puzzle.game.get_title(self.language)
			
		else :
			text = self.puzzle.text


		self.draw_back()
	
		
	def was_something_clicked(self, (x, y), mousebutton) :
	
		clicked = ui.Page.was_something_clicked(self, (x,y), mousebutton)		
	
		if (clicked != None) :
			(component_clicked, foo, dirty1) = clicked	
			
			if ((self.dragged_sprite == None) and (self.puzzle.done == False)) :
				# this might be a puzzle piece to drag
				
				for puzzle_piece in self.puzzle_pieces :
					
					if (component_clicked == puzzle_piece) :
	
						dirty2 = self.remove(component_clicked)
			
						sprite = ui.Sprite(component_clicked)
			
						self.set_dragged_sprite(sprite, (x, y))
			
						return(component_clicked, None, dirty1 + dirty2)
	
	
	
		return clicked

	def undrag_sprite(self) :
		
		puzzle_piece_dragged = self.dragged_sprite.component
		
		for puzzle_piece in self.puzzle_pieces :
		
			empty_location = puzzle_piece.associated_object
						
			if (empty_location.rect.colliderect(puzzle_piece_dragged)) :
				
				common_rect = puzzle_piece_dragged.rect.clip(empty_location.rect)
				
				if ((common_rect.width > empty_location.rect.width * self.drag_precision) and (common_rect.height > empty_location.rect.height * self.drag_precision)) :
				
					puzzle_piece_dragged.rect = copy.copy(empty_location.rect)
					
					
					for other_piece in self.puzzle_pieces :
						if (puzzle_piece_dragged.rect == other_piece.rect) :
							if (puzzle_piece_dragged != other_piece) :
								# we collide with another piece
								# so we go back to initial place
								puzzle_piece_dragged.rect = self.dragged_sprite.initial_pos
								
								self.play_error_sound()
								
								break
					
					break
				
	
		

		self.append(puzzle_piece_dragged)

		# we check the pieces, the puzzle might be ended ?
		all_ok = True
		for puzzle_piece in self.puzzle_pieces :
			if (puzzle_piece.associated_object.rect != puzzle_piece.rect) :
				all_ok = False
				break
		
		dirty_rects = []
	
		if (all_ok == True) :

			self.game.stop_timer()
			
			self.puzzle.done = True
			
			self.play_congratulations_sound()
		
			self.append(self.next_icon)

			dirty_rects = self.next_icon.draw()
		
		self.set_dragged_sprite(None)			
		
		return dirty_rects + puzzle_piece_dragged.draw()



class Puzzle() :
	def __init__(self, game) :
		self.game = game

		self.image = ""
		
		self.text = ""

		self.done = False
		
		self.pieces_amount_x = 0
		self.pieces_amount_y = 0
		
class Puzzle_game(common.Game) :

	def __init__(self, game, lang, score) :

		self.globalvars = game.globalvars
		
		# creation of a new game
		common.Game.__init__(self, self.globalvars, game.xml_game_node, game.level, score)

		self.score.enable_record_time()


		if (self.xml_game_node != None) :

			# reading global parameters
			xml_global_parameters_node = self.xml_game_node.getElementsByTagName("global_parameters")[0]
		
			# first of all, game setup
			xml_game_setup_node = self.xml_game_node.getElementsByTagName("game_setup")[0]
			
			# the default amount of pieces on x and y axis
			self.pieces_amount_x = xml_funcs.getInt(xml_game_setup_node.getElementsByTagName("pieces_amount_x")[0])
			self.pieces_amount_y = xml_funcs.getInt(xml_game_setup_node.getElementsByTagName("pieces_amount_y")[0])

			# eventual setup for placeholders
			self.goal_image_file = constants.puzzle_tux_image

			goal_nodes = xml_global_parameters_node.getElementsByTagName("goal")
			if (len(goal_nodes) > 0) :
				goal_node = goal_nodes[0]
				
				image_file_nodes = goal_node.getElementsByTagName("image")
		
				if (len(image_file_nodes) > 0) :
					self.goal_image_file = xml_funcs.getText(image_file_nodes[random.randint(0, len(image_file_nodes)-1)])

								
			# reading puzzle items
			
			main_puzzles = self.xml_game_node.getElementsByTagName("puzzles")[0]
			
			puzzle_nodes = main_puzzles.getElementsByTagName("puzzle")
			
			self.puzzles = []
			
			for puzzle_node in puzzle_nodes :
				
				puzzle = Puzzle(self)
				
				image_nodes = puzzle_node.getElementsByTagName("image")
				
				puzzle.image = xml_funcs.getText(image_nodes[0])
				
				sound_nodes = puzzle_node.getElementsByTagName("sound")
					
				if len(sound_nodes) > 0 :
					puzzle.sound = xml_funcs.getText(sound_nodes[0])

				text_nodes = puzzle_node.getElementsByTagName("text")
				
				if len(text_nodes) > 0 :
					
					for text_node in text_nodes :

						lang_attr = text_node.getAttribute("lang")
						
						if (lang_attr == "") :
							# if no "lang" attribute, we assume
							# the language of the text is the one expected
							puzzle.text = xml_funcs.getText(text_node)
						
						if (cmp(lang_attr, lang) == 0) :
							# if we have the correct language, we
							# take the text and exit the loop
							puzzle.text = xml_funcs.getText(text_node)
							break
					
				if (puzzle.pieces_amount_x == 0) :
					puzzle.pieces_amount_x = self.pieces_amount_x
				
				if (puzzle.pieces_amount_y == 0) :
					puzzle.pieces_amount_y = self.pieces_amount_y
					
				self.puzzles.append(puzzle)
				
			self.puzzles = common.randomize_list(self.puzzles)
	
	def get_puzzle(self) :
		# returning a puzzle
		for puzzle in self.puzzles :
			if (puzzle.done == False) :
				return puzzle
		else :
			# no more puzzles to do
			return None


def next_page(game, globalvars) :

	next_puzzle = game.get_puzzle()
	
	game.rounds_done = game.rounds_done + 1
	
	if ((next_puzzle <> None) and (game.rounds_done < game.rounds_amount + 1)) :

		current_page = Page_basic_puzzle(globalvars, next_puzzle, game)
	
		current_page.draw()
		pygame.display.flip()

		game.start_timer()

		return current_page

	else :
		common.info("Game over: no more puzzles !")
		
		return None


class Run_Puzzle_Screen(common.Run_Screen) :

	def __init__(self, game, globalvars, total_score) :
	
		common.info("Running puzzle activity")

		game = Puzzle_game(game, globalvars.main_language, total_score)

		common.Run_Screen.__init__(self, globalvars, game)	

		self.current_page = next_page(self.game, globalvars)
	

		while self.running :

			common.Run_Screen.run_pre(self)

			# actions after keyboard events

			for key_event in self.key_events :
								
				if key_event.key == K_SPACE :
					if (self.current_page.puzzle.done == True) :
						self.current_page.fade_out()
						self.current_page = next_page(self.game, globalvars)
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
						self.current_page.fade_out()
						self.current_page = next_page(self.game, globalvars)

						if (self.current_page == None) :
							return
		
					self.dirty_rects = self.dirty_rects + some_dirty_rects
		
			common.Run_Screen.run_post(self)
		
