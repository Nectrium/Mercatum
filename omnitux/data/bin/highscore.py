# -*- coding: utf-8 -*-

# Omnitux - educational activities based upon multimedia elements
# Copyright (C) 2010 Olav_2 (ol_av_2-omnitux@yahoo.fr)
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

import pygame, os, random, traceback, xml.dom, xml.dom.minidom, xml_funcs, time, calendar
from pygame.locals import *
			
import ui, constants, common


class Page_highscore(ui.Page) :


	def __init__(self, globalvars) :
		
		self.dragged_sprite = None
		self.draggable_items = []
	
		background = constants.highscore_background_file
	
		self.find_tuxes()

		self.scores = None

		ui.Page.__init__(self, globalvars, background)

		self.add_tuxes()

		self.draw_back()

	
	def add_tuxes(self) :

		size = (14, 7)
		step = 3


		# tuxes sitting at the top

		coords = (1.25, 81.25)
		for p in range(23) :
			self.append_back(ui.Image(self, coords, size, self.tuxes[random.randint(0, len(self.tuxes)-1)]))
			(x, y) = coords
			coords = (x + step, y)


		coords = (76, 81.25)
		for p in range(6) :
			self.append_back(ui.Image(self, coords, size, self.tuxes[random.randint(0, len(self.tuxes)-1)]))
			(x, y) = coords
			coords = (x + step, y)


		# one line below

		coords = (-7, 85)
		self.append_back(ui.Image(self, coords, size, self.tuxes[random.randint(0, len(self.tuxes)-1)]))


		coords = (2.75, 85)
		for p in range(14) :
			self.append_back(ui.Image(self, coords, size, self.tuxes[random.randint(0, len(self.tuxes)-1)]))
			(x, y) = coords
			coords = (x + step, y)


		coords = (53.25, 85)
		for p in range(7) :
			self.append_back(ui.Image(self, coords, size, self.tuxes[random.randint(0, len(self.tuxes)-1)]))
			(x, y) = coords
			coords = (x + step, y)

		coords = (77.5, 85)
		for p in range(6) :
			self.append_back(ui.Image(self, coords, size, self.tuxes[random.randint(0, len(self.tuxes)-1)]))
			(x, y) = coords
			coords = (x + step, y)


		# another line below
		coords = (-5.5, 90)
		for p in range(2) :
			self.append_back(ui.Image(self, coords, size, self.tuxes[random.randint(0, len(self.tuxes)-1)]))
			(x, y) = coords
			coords = (x + step, y)

		coords = (4.25, 90)
		for p in range(13) :
			self.append_back(ui.Image(self, coords, size, self.tuxes[random.randint(0, len(self.tuxes)-1)]))
			(x, y) = coords
			coords = (x + step, y)

		coords = (54.75, 90)
		for p in range(7) :
			self.append_back(ui.Image(self, coords, size, self.tuxes[random.randint(0, len(self.tuxes)-1)]))
			(x, y) = coords
			coords = (x + step, y)

		coords = (79, 90)
		for p in range(6) :
			self.append_back(ui.Image(self, coords, size, self.tuxes[random.randint(0, len(self.tuxes)-1)]))
			(x, y) = coords
			coords = (x + step, y)

		# last line at the bottom
		coords = (-7, 95)
		for p in range(3) :
			self.append_back(ui.Image(self, coords, size, self.tuxes[random.randint(0, len(self.tuxes)-1)]))
			(x, y) = coords
			coords = (x + step, y)

		coords = (5.75, 95)
		for p in range(13) :
			self.append_back(ui.Image(self, coords, size, self.tuxes[random.randint(0, len(self.tuxes)-1)]))
			(x, y) = coords
			coords = (x + step, y)

		coords = (53.25, 95)
		for p in range(8) :
			self.append_back(ui.Image(self, coords, size, self.tuxes[random.randint(0, len(self.tuxes)-1)]))
			(x, y) = coords
			coords = (x + step, y)

		coords = (80.5, 95)
		for p in range(6) :
			self.append_back(ui.Image(self, coords, size, self.tuxes[random.randint(0, len(self.tuxes)-1)]))
			(x, y) = coords
			coords = (x + step, y)




	def update(self) :
		
		ui.Page.update(self)


		self.display_scores()

		self.next_icon = ui.Image(self, constants.go_next_icon_pos, constants.go_next_icon_size, constants.go_next_icon)
		self.append(self.next_icon)


	def display_scores(self) :

		self.remove_all()

		(init_score_x, score_y) = constants.highscore_pos

		(score_width, score_height) = constants.highscore_size


		step = score_height / constants.max_highscores


		if (self.scores != None) :

			if (len(self.scores.scores) > 0) :

				name_ratio = 0.50

				if (self.scores.scores[0].count_good == True) :
					good_answers_ratio = 0.15
				else :
					name_ratio = name_ratio + 0.15
					good_answers_ratio = 0


				if (self.scores.scores[0].count_wrong == True) :
					wrong_answers_ratio = 0.15
				else :
					name_ratio = name_ratio + 0.15
					wrong_answers_ratio = 0
	

				if (self.scores.scores[0].record_time == True) :
					time_ratio = 0.20
				else :
					name_ratio = name_ratio + 0.20
					time_ratio = 0


				index_color = 0

				for score in self.scores.scores :

					color = constants.legend_text_colors[index_color]

					index_color = index_color + 1
				
					if (index_color >= len(constants.legend_text_colors)) :
						index_color = 0


					score_x = init_score_x

					name = score.get_name()

					good_answers = str(score.get_good_answers_value())

					wrong_answers = str(score.get_wrong_answers_value())

					time = score.get_time_toString()
				

					self.append(ui.Text(self, name, (score_x, score_y), (score_width * name_ratio, step), self.fonts, color, 0))
					score_x = score_x + score_width * name_ratio


					if (good_answers_ratio != 0) :
						self.append(ui.Text(self, good_answers, (score_x, score_y), (score_width * good_answers_ratio, step), self.fonts, color, 1))
						score_x = score_x + score_width * good_answers_ratio


					if (wrong_answers_ratio != 0) :
						self.append(ui.Text(self, wrong_answers, (score_x, score_y), (score_width * wrong_answers_ratio, step), self.fonts, color, 1))
						score_x = score_x + score_width * wrong_answers_ratio


					if (time_ratio != 0) :
						self.append(ui.Text(self, time, (score_x, score_y), (score_width * time_ratio, step), self.fonts, color, 1))



					score_y = score_y + step



	def find_tuxes(self) :

		tuxes = common.get_files(constants.folder_award_tuxes, constants.image_extensions)
		
		self.tuxes = common.randomize_list(tuxes)


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
	
	
class Highscores() :

	def __init__(self, globalvars, level, total_score) :

		self.globalvars = globalvars
		self.level = level

		self.language = self.globalvars.main_language

		self.game_set = self.level.game_set
		self.game_set_filename = self.level.game_set.xml_filename


		# replaces ".." (up directory) by "UPupO" (hopefully never used in a dir name !)
		self.game_set_filename_nodots = self.game_set_filename.replace("..", "UPupO")


		self.title = self.game_set.get_title(self.language)
		self.game_set_icon_file = self.game_set.get_thumb()
		
		self.difficulty = self.level.get_difficulty()
		self.level_icon_file = self.level.get_difficulty_level_image()

		self.highscore_filename = os.path.join(constants.highscore_dir, self.game_set_filename_nodots, self.language, self.difficulty, "high.hxml")


		self.scores = []		

		self.load()

		if (total_score != None) :
			self.new_score_index = self.add_score(total_score)

			print "high index :"

			print self.new_score_index


	def load(self) :
		
		try :
			xml_data = xml.dom.minidom.parse(self.highscore_filename)

			highscore_nodes = xml_data.getElementsByTagName("highscore")

			for highscore_node in highscore_nodes :

				score = common.Score(self.globalvars)

				score.load_from_xml_node(highscore_node)

				self.add_score(score)

			xml_data.unlink()


		except Exception, e :

			common.error("Could not load highscore file")
			common.error(self.highscore_filename)
			common.error("Exception fired", e, traceback.format_exc())	


	def add_score(self, score) :

		self.scores.append(score)

		self.scores.sort(common.score_cmp)

		index = self.scores.index(score)

		if (index > constants.max_highscores) :
			index = constants.max_highscores

		return (index)


	def save(self) :

		try :

			
			impl = xml.dom.getDOMImplementation()
	
			xml_data = impl.createDocument(constants.namespace, u"omnitux_highscores", None)

			root_node = xml_data.documentElement

			root_node.setAttribute(u"Version", constants.version)


			for score in self.scores :

				score_node = xml_data.createElement("highscore")

				score_node.setAttributeNode(xml_data.createAttribute("name"))
				score_node.setAttribute("name", score.get_name())

				score_node.setAttributeNode(xml_data.createAttribute("datetime"))
				score_node.setAttribute("datetime", str(score.datetime))

				if (score.count_good == True) :
					score_node.setAttributeNode(xml_data.createAttribute("good_answers"))
					score_node.setAttribute("good_answers", str(score.get_good_answers_value()))

				if (score.count_wrong == True) :
					score_node.setAttributeNode(xml_data.createAttribute("wrong_answers"))
					score_node.setAttribute("wrong_answers", str(score.get_wrong_answers_value()))

				if (score.record_time == True) :
					score_node.setAttributeNode(xml_data.createAttribute("time"))
					score_node.setAttribute("time", str(score.timer.getValue()))

				root_node.appendChild(score_node)

			xml_funcs.save_xml_file(self.highscore_filename, xml_data)


		except Exception, e :

			common.error("Could not save highscore file")
			common.error(self.highscore_filename)
			common.error("Exception fired", e, traceback.format_exc())	



def create(globalvars) :

	highscore_page = Page_highscore(globalvars)	
	
	return highscore_page


class Run_Highscore(common.Run_Screen) :

	def __init__(self, highscore_page, level, total_score) :

		common.info("Running Highscore")

		self.current_page = highscore_page

		# TODO clean
		if (total_score != None) :
			total_score.datetime = calendar.timegm(time.gmtime())

		highscores = Highscores(self.current_page.globalvars, level, total_score)

		self.current_page.scores = highscores
		self.current_page.update()

		common.Run_Screen.__init__(self, self.current_page.globalvars)	

		
		highscore_page.draw()
		pygame.display.flip()
		

		while self.running :

			try :

				common.Run_Screen.run_pre(self)

			except common.EndActivityException, e :
					self.running = False
	
	
			# actions for mouse actions
			if (self.mouse_clicked == True) :
			
				clicked = highscore_page.was_something_clicked(self.mouse_pos, self.mousebutton)
					
				if (clicked != None) :
					(component_clicked, foo, some_dirty_rects) = clicked

					self.dirty_rects = self.dirty_rects + some_dirty_rects
						
					if (component_clicked == highscore_page.next_icon) :
						self.running = False
						
			# actions for keyboard
			for key_event in self.key_events :

				if (key_event.key == K_SPACE) :		

					self.running = False
		
						

			common.Run_Screen.run_post(self)

		# that's the end
		highscores.save()


		
